#! /bin/bash

set -e -o pipefail

uv run ruff check --fix
uv run pyright
uv run ruff format
uv run pytest
