from pydantic import BaseModel, Field
from prompts import static_webpage_prompt, streamlit_prompt, svg_prompt, vue_app_prompt


class ArtifactMetadata(BaseModel):
    name: str = Field(description="The name of the artifact.")
    prompt: str = Field(description="The prompt used to generate the artifact.")
    code_block_type: str = Field(
        description="The type of code block (e.g., python, html, vue)."
    )
    file_name: str | None = Field(
        default=None, description="The name of the file to be generated."
    )
    image_name: str | None = Field(
        default=None, description="The name of the Docker image for the artifact."
    )
    host_port: int | None = Field(
        default=None, description="The host port to expose the container."
    )
    container_port: int | None = Field(
        default=None, description="The container's internal port."
    )
    container_command: list[str] | None = Field(
        default=None, description="The command to run inside the container."
    )
    file_path: str | None = Field(
        default=None, description="The file path where the artifact will be saved."
    )


artifact_selector = {
    "Streamlit": ArtifactMetadata(
        name="streamlit",
        prompt=streamlit_prompt,
        code_block_type="python",
        container_port=8500,
        host_port=8500,
        file_name="run.py",
        image_name="streamlit-image-artifact:latest",
        container_command=[
            "streamlit",
            "run",
            "run.py",
            "--server.port=8500",
            "--server.address=0.0.0.0",
        ],
    ),
    "Static": ArtifactMetadata(
        name="static",
        prompt=static_webpage_prompt,
        code_block_type="html",
        file_name="index.html",
        container_port=8080,
        host_port=8080,
        image_name="static-image-artifact",
    ),
    "Vue": ArtifactMetadata(
        name="vue",
        prompt=vue_app_prompt,
        code_block_type="vue",
        file_name="App.vue",
        container_port=3000,
        host_port=3000,
        image_name="vue-image-artifact",
    ),
    "SVG": ArtifactMetadata(
        name="static",  # same name as `static` to auto remove the container, since uses the same port
        prompt=svg_prompt,
        code_block_type="html",
        file_name="index.html",
        container_port=8080,
        host_port=8080,
        image_name="static-image-artifact",
    ),
}
