# URLoad

An interactive CLI tool for scraping websites.

## Code style and structure

- Follow PEP 8 for Python code style.
- Use type hints for function signatures.
- All public functions and classes must have docstrings.
  - Follow PEP 257 for docstring conventions.
  - Describe each parameter and return value in the docstring, but do not
    repeat the parameter types in the docstring.
  - Include any exceptions that the function may raise in the docstring. Use
    `:raises CommandError:` for user-facing errors.

## Dependency management

- Use `uv` to manage dependencies. Do not use `pip` directly.
- Add new dependencies using `uv add <package>` or `uv add --dev <package>` in
  the case of a development-only dependency.
- Do not modify `uv.lock` directly; it is managed by `uv`.

## Testing

- Use `pytest` for testing.
- Tests should be placed in the `tests` directory.
- After each change, do the following, in order. Do not skip or combine any steps:
  - Run the linter, `uv run ruff check`, fix any issues it reports, and rerun.
  - Run the type checker, `uv run pyright`, fix any issues it reports, and rerun.
  - Run the tests, `uv run pytest`, and ensure all tests pass.
  - Run the formatter, `uv run ruff format`.
