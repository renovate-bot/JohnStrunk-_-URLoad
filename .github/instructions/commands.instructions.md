---
description: Instructions for creating and modifying URL commands.
applyTo: src/urload/commands/*.py
---

# Instructions for Creating and Modifying URL Commands

## Command Structure

- Each command must be implemented as a class that inherits from `Command` in
  `base.py`.
- The command class should be named with the pattern `NameCommand` (for
  example, `AddCommand`, `DelCommand`).
- Each command must define:
  - `name`: the command's string identifier (for example, `"add"`, `"del"`).
  - `description`: a multi-line string (use `textwrap.dedent`) describing
    usage and behavior. The first line should be a short usage line, with the
    name of the command and a brief description. A more detailed description
    should follow. For example:

    ```python
    description = textwrap.dedent("""
    add <url> - Add a URL to the list

    This command allows you to add a URL to your current list of URLs.
    """)
    ```

  - A `run(self, args: list[str], url_list: list[URL]) -> list[URL]` method
    that implements the command logic.
- All public classes and methods must have reStructuredText docstrings.
- Use type hints for all function signatures.
- Raise `CommandError` (from `base.py`) for user-facing errors (such as
  invalid arguments).

## Imports and Dependencies

- Import only what is needed. Use standard library modules where possible.
- Import `Command` and `CommandError` from `urload.commands.base`.
- Import `URL` from `urload.url`.

## Command Behavior

- Commands should not mutate the input `url_list` unless mutation is the
  intended effect (for example, `add`, `del`). If returning a new list, do not
  return the original object.
- Print user-facing output (such as confirmation, errors) as appropriate for
  the command.
- Validate all arguments and provide clear error messages.
- Use regular expressions for pattern-based commands (such as `keep`,
  `discard`) and handle invalid regex with `CommandError`.

## Consistency

- Follow PEP 8 for code style.
- Use consistent naming and structure across all commands.
- Use `textwrap.dedent` for multi-line descriptions.
- Place all command classes in their own file named after the command (for
  example, `add.py`, `del.py`).

## Testing

- Each command must have a corresponding test file in `tests/` named
  `test_<command>_command.py`.
- Use `pytest` for all tests.
- Test files should:
  - Test normal operation, edge cases, and error handling.
  - Use fixtures like `capsys` to capture and assert printed output.
  - Use `pytest.raises` to check for `CommandError` on invalid input.
  - Test that the command does not mutate the input list unless intended.
- Ensure all tests pass after changes.

## Documentation

- The first line of each command file should be a module docstring describing
  the command.
- The `description` attribute should provide both a short usage line and a
  longer explanation.
