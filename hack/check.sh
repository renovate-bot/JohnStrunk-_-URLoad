#! /bin/bash

set -e -o pipefail

uv run ruff check --fix -q || { rc=$?; echo "*** ruff check failed ***"; exit $rc; }
uv run pyright || { rc=$?; echo "*** pyright failed ***"; exit $rc; }
uv run ruff format -q || { rc=$?; echo "*** ruff format failed ***"; exit $rc; }
uv run pytest || { rc=$?; echo "*** pytest failed ***"; exit $rc; }

echo "All checks passed successfully."
