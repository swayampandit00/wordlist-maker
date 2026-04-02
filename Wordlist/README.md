# Wordlist Maker

A powerful password wordlist generator tool that creates customized password lists based on personal information, dates, phone numbers, and other custom data.

## Features

- **Smart Permutation Generation**: Creates various combinations of names, dates, phone numbers, and keywords
- **Customizable Complexity Levels**: 6 different complexity levels from simple to nuclear
- **Flexible Configuration**: Adjustable password length, character sets, and generation options
- **Leet Speak Support**: Optional leet permutations for enhanced password variations
- **Memory Efficient**: Streams large results to file without consuming excessive RAM

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd wordlist
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the tool and follow the interactive prompts:

```bash
python wordlist.py
```

### Command Line Options

```bash
python wordlist.py [OPTIONS]
```

**Available Options:**
- `-l, --level`: Complexity level (0-5, default: 0)
- `--min`: Minimum password length (default: 8)
- `--max`: Maximum password length (default: 12)
- `-r, --num-range`: Number range to include (0 to specified number)
- `--leet`: Enable leet permutations
- `-y, --years`: Include years from specified year to current year
- `-c, --chars`: Include special characters
- `-v, --verbose`: Show passwords during generation
- `-x, --export`: Output filename (default: passwords.txt)

### Examples

**Simple wordlist:**
```bash
python wordlist.py -l 0 --min 6 --max 10
```

**Advanced wordlist with all features:**
```bash
python wordlist.py -l 5 --min 8 --max 16 -r 999 -y 1990 --leet --chars -v
```

**Custom output file:**
```bash
python wordlist.py -x my_wordlist.txt
```

## Complexity Levels

- **Level 0**: Simple person - Basic permutations
- **Level 1**: Average person - More permutation options
- **Level 2**: Cyber awareness - Enhanced old password permutations
- **Level 3**: Paranoid person - Full special character set
- **Level 4**: Nerd person - Advanced permutation combinations
- **Level 5**: Nuclear! - Maximum permutations without ordered pairs

## Input Format

During interactive mode, provide:

1. **Names**: Comma-separated names (no spaces)
2. **Keywords**: Nicknames, jobs, movies, series (comma-separated)
3. **Dates**: Format dd-mm-yyyy (comma-separated)
4. **Phone Numbers**: Format +CountryCodeNumber (comma-separated)
5. **Old Passwords**: Previous passwords or base words (comma-separated)

## Output

The tool generates:
- Primary wordlist file (default: `passwords.txt`)
- Optional leet permutations file (prefixed with `Leeted-`)
- Generation statistics and performance metrics

## Next Updates

### Planned Features:
- **GUI Interface**: User-friendly graphical interface for easier operation
- **More Language Support**: Support for non-English characters and patterns
- **Pattern Templates**: Pre-defined templates for common password patterns
- **Import/Export**: Ability to save and load generation configurations
- **Performance Optimization**: Multi-threading for faster generation
- **Wordlist Analysis**: Built-in analysis tools for generated wordlists

### How to Use Future Updates:
1. **GUI Interface**: Simply run `python gui.py` (when available) for a visual interface
2. **Pattern Templates**: Use `-t` or `--template` flag with template names
3. **Configuration**: Save settings with `--save-config filename` and load with `--load-config filename`
4. **Multi-threading**: Use `--threads N` to specify number of threads for faster generation

## Requirements

- Python 3.6+
- See `requirements.txt` for detailed dependencies

## License

This tool is for educational and authorized security testing purposes only. Users are responsible for ensuring compliance with applicable laws and regulations.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
