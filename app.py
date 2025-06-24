import os
from io import BytesIO
import re
import shutil
import tempfile
import time
from typing import Generator

import docker
import docker.errors
import streamlit as st
import streamlit.components.v1 as components
from docker.types import Mount
from openai import OpenAI

from layout import unified_iframe_html
from models import ArtifactMetadata, artifact_selector


# ------- SESSION STATE ------- #
def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "selectbox_disabled" not in st.session_state:
        st.session_state.selectbox_disabled = False


def disable_selector():
    st.session_state.selectbox_disabled = True


# ------- DOCKER OPERATIONS ------- #
def execute_docker(
    host_path: str,
    artifact_metadata: ArtifactMetadata,
    container_path: str = "/home/runner/app",
):
    client = docker.from_env()
    mount = Mount(target=container_path, source=host_path, type="bind", read_only=False)
    try:
        container = client.containers.run(
            image=artifact_metadata.image_name,
            mounts=[mount],
            ports={str(artifact_metadata.container_port): artifact_metadata.host_port},
            detach=True,
            name=f"llm-artifact-{artifact_metadata.name}",
        )
        st.session_state["container_id"] = container.id
        return container.id
    except docker.errors.DockerException as e:
        st.toast(str(e), icon="❌")
        print("❌ Error", str(e))
        st.stop()


def stop_container(container_name: str):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        return f"Container '{container_name}' stopped and removed successfully."
    except docker.errors.NotFound:
        return f"Container '{container_name}' not found."
    except Exception as e:
        return f"Failed to stop the container: {str(e)}"


def download_project_archive():
    client = docker.from_env()
    container_id = st.session_state.get("container_id")
    if not container_id:
        st.toast(
            "Cannot download files at the moment, container_id not found.", icon="❌"
        )
        return

    container = client.containers.get(container_id)
    try:
        stream, stat = container.get_archive("/home/runner/app")
        tar_data = BytesIO()
        for chunk in stream:
            tar_data.write(chunk)
        tar_data.seek(0)
        return tar_data
    except docker.errors.APIError as e:
        print(f"Error downloading project files from container: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# ------- LLM OPERATIONS ------- #
def get_code_group(llm_response: str, code_block: str) -> str | bool:
    code_match = re.search(rf"```{code_block}\s*(.*?)\s*```", llm_response, re.DOTALL)
    if not code_match:
        msg = "Regex: No code group found in the response."
        print("❌", msg)
        st.toast(msg, icon="❌")
        st.stop()

    return code_match.group(1).strip()


def call_llm(prompt: str, system_prompt: str) -> Generator[str, None, None]:
    if st.session_state.get("local_mode", False):
        client = OpenAI(base_url="http://localhost:11434/v1")
        model = "llama3.2:3b"
    else:
        client = OpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        model = "gemini-2.0-flash"

    chat_history = st.session_state.get("messages", [])
    messages = (
        [{"role": "system", "content": system_prompt}]
        + chat_history
        + [{"role": "user", "content": prompt}]
    )

    response = client.chat.completions.create(
        model=model, messages=messages, stream=True
    )
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


# ------- UI ------- #
def render_in_iframe(url: str):
    time.sleep(3)  # to let the server run in Docker
    print("Rendering in iFrame....", url)
    with tab2:
        components.html(
            unified_iframe_html.format(src=url),
            height=800,
            scrolling=True,
        )
    st.toast(f"Application running on: {url}", icon="🚀")


def handle_renders(artifact_metadata: ArtifactMetadata):
    web_address = None
    match artifact_metadata.name:
        case "static" | "svg" | "streamlit":
            execute_docker(
                host_path=os.path.dirname(artifact_metadata.file_path),
                artifact_metadata=artifact_metadata,
            )
        case "vue":
            execute_docker(
                host_path=artifact_metadata.file_path,
                artifact_metadata=artifact_metadata,
                container_path="/home/runner/app/src/App.vue",
            )
    if artifact_metadata.host_port:
        web_address = f"http://localhost:{artifact_metadata.host_port}"
        render_in_iframe(web_address)


# ------- MAIN APPLICATION BLOCK ------- #
if __name__ == "__main__":
    st.set_page_config(page_title="LLM with Artifact Generation", layout="wide")
    init_session()
    col1, col2 = st.columns([3, 6])
    with col2:
        tab1, tab2 = st.tabs(["Code", "Preview"])

    with tab1:
        messages = st.container()
        with messages:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

    with col1:
        st.header("✨LLM Artifact Generation")
        artifact_type_selector = st.selectbox(
            label="Artifact type",
            options=("Streamlit", "Vue", "Static", "SVG"),
            index=0,
            disabled=st.session_state.get("selectbox_disabled", False),
        )
        artifact_metadata = artifact_selector[artifact_type_selector]
        prompt = st.chat_input(
            placeholder="⌨️ Enter your prompt", on_submit=disable_selector
        )
        st.toggle("Use Local Models", value=False, key="local_mode")
        st.write("##")
        reset = st.button("↻ Reset Application")
        download_files = st.button(
            "⇊ Download Files",
        )
        container_name = f"llm-artifact-{artifact_metadata.name}"

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = call_llm(prompt=prompt, system_prompt=artifact_metadata.prompt)

        with col2:
            messages.chat_message("user").write(prompt)
            llm_response = messages.chat_message("ai").write_stream(response)
            print("Raw LLM Response: ", llm_response)
            generated_code = get_code_group(
                llm_response=llm_response,
                code_block=artifact_metadata.code_block_type,
            )
            print("regex got code group: ", generated_code)

        if generated_code and artifact_metadata.file_name:
            st.session_state.messages.append(
                {"role": "assistant", "content": llm_response}
            )
            temp_dir = tempfile.mkdtemp()
            temp_dir_file_path = f"{temp_dir}/{artifact_metadata.file_name}"

            with open(temp_dir_file_path, "w") as f:
                f.write(generated_code)

            artifact_metadata.file_path = temp_dir_file_path

            with col2:
                stop_container(container_name)  # remove any existing containers
                handle_renders(artifact_metadata)

    if reset:
        stop_container(container_name)
        st.session_state.clear()
        file_path = artifact_metadata.file_path
        if file_path and os.path.exists(file_path):
            shutil.rmtree(os.path.dirname(file_path), ignore_errors=True)
        st.rerun()

    if download_files:
        archive = download_project_archive()
        st.download_button(
            label="Download Project File",
            data=archive,
            file_name="project.tar",
            mime="application/x-tar",
            icon=":material/download:",
        )
