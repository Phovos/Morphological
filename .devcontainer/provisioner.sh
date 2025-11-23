#!/usr/bin/env bash
set -euo pipefail

echo "> Provisioning devcontainer"

export UV_LINK_MODE=copy

echo "> Creating fresh .venv"
uv venv .venv --clear --python 3.14.0

echo "> Installing JupyterLab 4.5.0 + ipykernel"
uv pip install --upgrade pip
uv pip install "jupyterlab==4.5.0" ipykernel

echo "> Registering kernel"
source .venv/bin/activate
python -m ipykernel install \
    --user \
    --name=project \
    --display-name="Project (uv)"
deactivate

echo "> Provisioning finished"

# uv run jupyter lab --no-browser --ip=0.0.0.0 --port=8888
# "portsAttributes": {
#   "8228": { "label": "App Server", "onAutoForward": "openBrowser" },
#   "8888": { "label": "Jupyter", "onAutoForward": "notify" }
# }
