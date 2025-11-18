#!/bin/bash
FILE=$1
# /.devcontainer/setup.sh
set -e  # Exit on any error

echo "Setting up the Morphological-Source-Code dev environment..."

# UNUSED::Seperate .env for each branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" == "staging" ]]; then
    cp env.example .env
elif [[ "$BRANCH" == "development" ]]; then
    cp env.example .env
elif [[ "$BRANCH" == "production" ]]; then
    cp env.example .env
else
    cp env.example .env
fi

# Generate JupyterLab configuration
uv run -m jupyterlab --generate-config

# Create a Jupyter kernel for this environment
uv run -m ipykernel install --user --name=morphological

# Optional: Add any additional setup steps here

echo "Starting JupyterLab..."
echo "Setup complete. JupyterLab will start now."
exec uv run --with jupyter jupyter lab --ip=0.0.0.0 --port=8888 --allow-root

sleep 1

source .bashrc

# "portsAttributes": {
#   "8000": { "label": "App Server", "onAutoForward": "openBrowser" },
#   "8888": { "label": "Jupyter", "onAutoForward": "notify" }
# }
