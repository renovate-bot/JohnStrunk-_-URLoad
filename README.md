# URLoad

URLoad is an interactive CLI tool for scraping websites, designed to make
extracting and managing web data simple and efficient.

## Features

- Interactive command-line interface for scraping and processing URLs
- Modular commands for extracting links, images, and other web content
- Easy-to-use options for saving, sorting, and filtering results
- Configurable settings saved in `urload.toml`
- Extensible architecture for adding new commands

## Installation

```console
pip install --user urload
```

## Usage

Start the interactive CLI:

```console
$ urload
Welcome to URLoad! Type 'help' for commands.
Current session directory: 0000
URLoad (0) >
```

### Common Commands

- `add <url>`: Add a URL to the current list
- `list`: List all URLs
- `get`: Fetch all URLs in the current list
- `img <url>`: Extract image links from the current list
- `href <url>`: Extract hyperlinks from the current list
- `save <filename>`: Save the current URL list to a file
- `load <filename>`: Load the URL list from a file
- `sort`: Sort the URL list alphabetically
- `uniq`: Remove duplicate URLs
- `help`: Show help for commands

All commands can be explored interactively.

- Use `help` to list available commands.
- Use `help <command>` to get detailed help for a specific command.

## Development

The project uses [uv](http://astral.sh/uv) for dependency management.

To run the project locally, clone the repository and run with `uv`:

```console
git clone https://github.com/JohnStrunk/URLoad.git
cd URLoad
uv run urload
```

### Testing

To run all tests and code checks:

```console
./hack/check.sh
```

This will run linting, formatting, and all unit tests.

## License

**SPDX-License-Identifier:** AGPL-3.0-or-later

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
details.
