#! /bin/bash

set -e -o pipefail

uv run pytest
uv run pyright
uv run ruff check --fix
uv run ruff format
uv run pytest
