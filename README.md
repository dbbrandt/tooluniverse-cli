# ToolUniverse CLI

A powerful, enhanced command-line interface for ToolUniverse - a collection of 214+ biomedical tools designed for accessing biomedical data from multiple sources including FDA Drug Label data, OpenTargets, and Monarch Initiative.

## Features

- **Discover Tools**: Browse and search through hundreds of biomedical tools
- **Rich Output Formats**: View results in nicely formatted text tables or structured JSON
- **Category Management**: Easily filter tools by category (FDA, OpenTarget, Monarch)
- **Case-Insensitive Search**: Find tools regardless of capitalization
- **Detailed Documentation**: Get comprehensive information about tool parameters
- **Command Completion**: Bash/Zsh completion for commands and options
- **Visualization**: Format results for easier interpretation

## Installation

```bash
pip install tooluniverse-cli
```

## Usage

### List available tools

```bash
# List all tools
toolu list

# List tools by category
toolu list --category monarch

# Output as JSON
toolu list --format json
```

### Search for tools

```bash
# Search for tools matching a string
toolu search "drug abuse"

# Filter search by category
toolu search "phenotype" --category monarch

# Case-sensitive search
toolu search "HPO" --case-sensitive
```

### Get tool information

```bash
# Get detailed information about a specific tool
toolu info get_drug_names_by_abuse_info
```

### Call a tool

```bash
# Call a tool with arguments
toolu call get_drug_names_by_abuse_info abuse_type="misuse"
```

## Why a separate CLI?

This CLI builds on the foundation of ToolUniverse, offering enhanced usability, improved output formatting, and additional features while maintaining complete compatibility with the underlying ToolUniverse library.

## Requirements

- Python 3.8+
- ToolUniverse library
- Click
- Rich (for enhanced terminal output)
- Tabulate (for table formatting)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
