FROM public.ecr.aws/docker/library/python:3.11.11-slim-bookworm AS build

RUN <<eot
    set -ex

    groupadd -g 1000 runner
    useradd -m -u 1000 -g runner -d /home/runner runner

    su runner -c "pip install --no-cache-dir --user streamlit numpy pandas seaborn matplotlib pillow requests plotly beautifulsoup4 openai"
eot



FROM public.ecr.aws/docker/library/python:3.11.11-slim-bookworm

SHELL [ "/bin/bash", "-c" ]

RUN <<eot
    set -ex

    groupadd -g 1000 runner
    useradd -m -u 1000 -g runner -d /home/runner runner
    chown runner:runner /home/runner
eot

WORKDIR /home/runner/app

COPY --from=build --chown=runner:runner /home/runner/.local /home/runner/.local/


COPY <<EOF run.py
import streamlit as st

st.title('Hello World!')
st.write('Welcome to Streamlit app')
EOF

RUN <<eot

    set -ex

    mkdir -p /home/runner/.streamlit/
    cat <<EOF > /home/runner/.streamlit/config.toml
[server]
headless = true
enableXsrfProtection=false
enableCORS = true
EOF
eot

USER runner

ENV PATH=$PATH:/home/runner/.local/bin

EXPOSE 8500

ENTRYPOINT ["/home/runner/.local/bin/streamlit", "run", "run.py", "--server.port=8500", "--server.address=0.0.0.0"]
