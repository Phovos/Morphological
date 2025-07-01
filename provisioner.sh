echo "MY_VAR='Hello, world!'" > .env

uv run --env-file .env -- python -c 'import os; print(os.getenv("MY_VAR"))'

# uv run --with jupyter jupyter lab