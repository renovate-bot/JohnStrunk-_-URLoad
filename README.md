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
pip install --user git+https://github.com/JohnStrunk/urload
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

- `add <url>`: Add a URL to the session
- `list`: List all URLs in the session
- `get <url>`: Fetch and display content from a URL
- `img <url>`: Extract image links from a URL
- `href <url>`: Extract hyperlinks from a URL
- `save <filename>`: Save session data to a file
- `load <filename>`: Load session data from a file
- `sort`: Sort URLs or results
- `uniq`: Remove duplicate entries
- `help`: Show help for commands

All commands can be explored interactively. Use `help` for details on each
command.

## Development

The project uses [uv](http://astral.sh/uv) for dependency management.

To run the project locally, clone the repository and run with `uv`:

```console
uv run urload
```

### Testing

To run all tests and code checks:

```console
./hack/check.sh
```

This will run linting, formatting, and all unit tests.

---

See [LICENSE](LICENSE) for licensing information.
