#!/bin/bash
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

# Install Python dependencies and set up the environment
uv install --extra dev

# Generate JupyterLab configuration
uv run -m jupyterlab --generate-config

# Create a Jupyter kernel for this environment
uv run -m ipykernel install --user --name=morphological

# Run tests first (they might fail fast)
uv run -m nox -s tests

# Optional: Add any additional setup steps here

echo "Starting JupyterLab..."
echo "Setup complete. JupyterLab will start now."
exec uv run --with jupyter jupyter lab --ip=0.0.0.0 --port=8888 --allow-root