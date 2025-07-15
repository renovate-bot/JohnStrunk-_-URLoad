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
- After any change, run `./hack/check.sh` to ensure code style and linting
  checks pass.

## Dependency management

- Use `uv` to manage dependencies.
  - Do not use `pip` or `uv pip`.
  - Do not directly manage the virtual environment; `uv` handles this.
  - New packages can be added using `uv add <package>` or `uv add --dev
    <package>` if it is a development-only dependency.
- Do not modify `uv.lock` directly; it is managed by `uv`.

## Testing

- Use `uv run pytest` for testing.
- Tests should be placed in the `tests` directory.
- After adding or modifying code, write tests to cover the changes.
- Use `./hack/check.sh` to run all tests.
  - Fix any warnings or errors surfaced by the command.
  - Continue to run the command and fix issues until it passes by printing
    "All checks passed successfully."
