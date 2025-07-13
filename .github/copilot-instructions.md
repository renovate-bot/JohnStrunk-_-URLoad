# URLoad

An interactive CLI tool for scraping websites.

## Code style and structure

- Follow PEP 8 for Python code style.
- Use type hints for function signatures.
- All public functions and classes should have docstrings. Docstrings should be
  in reStructured text format, but do not repeat the parameter types in the
  docstring.
- `uv` is used to manage project dependencies.
  - Use `uv run urload` to run the application
  - Use `uv add <package>` to add a dependency or `uv add --dev <package>` if
  it's a development dependency.

## Testing

- Use `pytest` for testing.
- Tests should be placed in the `tests` directory.
- After each change:
  - Ensure the code is properly formatted with `uv run ruff format`.
  - Run the linter, `uv run ruff check`, and fix any issues it reports.
  - Run the type checker, `uv run pyright`, and fix any issues it reports.
  - Run the tests, `uv run pytest`, and ensure all tests pass.
