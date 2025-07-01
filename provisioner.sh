echo "MY_VAR='Hello, world!'" > .env

uv run --env-file .env -- python -c 'import os; print(os.getenv("MY_VAR"))'

# https://docs.astral.sh/uv/guides/integration/jupyter/#using-jupyter-within-a-project
# uv run --with jupyter jupyter lab
# uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=project
