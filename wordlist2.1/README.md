# 🔥 WORDLIST-MAKER 🔥

A powerful, feature-rich password wordlist generator with GUI and CLI interfaces, supporting multi-language patterns, advanced templates, multi-threading, and comprehensive analysis tools.

## 🚀 Features

- **🖥️ Dual Interface**: Modern GUI and powerful CLI
- **🌍 Multi-Language Support**: Hindi, Arabic, Chinese, Japanese, Russian, European characters
- **📋 Pattern Templates**: Pre-defined templates for common, corporate, personal, gaming, social passwords
- **⚡ Multi-Threading**: Parallel generation for maximum performance
- **📊 Analysis Tools**: Comprehensive wordlist analysis with recommendations
- **💾 Configuration Management**: Save/load settings for repeated use
- **🔄 Leet Permutations**: Automatic leet speak generation
- **🎯 Complexity Levels**: 6 levels from Simple to Nuclear!

## 📦 Installation

### Prerequisites
- Python 3.6+
- Git

### Quick Install
```bash
git clone <repository-url>
cd wordlist
pip install -r requirements.txt
```

### Dependencies
```bash
pip install colorama psutil click phonenumbers tkinter threading concurrent.futures unicodedata json queue re collections math
```

---

# 🖥️ GUI USAGE GUIDE

## 🚀 Getting Started with GUI

### Launch GUI
```bash
python gui.py
```

### GUI Interface Overview
The GUI is divided into three main sections:

1. **📝 Input Data Panel** (Left)
   - Names, Keywords, Dates, Phone Numbers, Old Passwords
   - Advanced Options (Languages, Templates, Performance)

2. **⚙️ Configuration Panel** (Right)
   - Complexity Levels, Password Length, Additional Options
   - Export File Settings

3. **📊 Output Console** (Bottom)
   - Real-time progress, Generation logs, Error messages

## 📚 Beginner GUI Guide

### Step 1: Basic Information Entry
1. **Names**: Enter target names separated by commas
   ```
   john,mary,admin,user
   ```

2. **Keywords**: Add relevant keywords
   ```
   company,project,2024,welcome
   ```

3. **Dates**: Add important dates (dd-mm-yyyy format)
   ```
   01-01-1990,15-08-2020,25-12-2023
   ```

4. **Phone Numbers**: Add known phone numbers
   ```
   +1234567890,+9876543210
   ```

5. **Old Passwords**: Add previous passwords if known
   ```
   password123,admin2023,welcome
   ```

### Step 2: Basic Configuration
1. **Complexity Level**: Start with Level 1 (Average)
2. **Password Length**: Set Min=8, Max=12
3. **Special Characters**: Enable this option
4. **Export File**: Keep default (passwords.txt)

### Step 3: Generate
1. Click **"Generate Wordlist"**
2. Watch progress in the console
3. Results saved to specified file

## 🚀 Advanced GUI Guide

### Multi-Language Support
Enable language support in the **Advanced Options** section:
- ✅ Hindi: For Devanagari script passwords
- ✅ Arabic: For Arabic character sets
- ✅ Chinese: For Chinese character combinations
- ✅ Japanese: For Hiragana/Katakana
- ✅ Russian: For Cyrillic scripts
- ✅ European: For European accented characters

### Pattern Templates
Select templates based on your target:
- ✅ **Common**: General password patterns
- ✅ **Corporate**: Business environment passwords
- ✅ **Personal**: Individual user passwords
- ✅ **Gaming**: Gaming platform passwords
- ✅ **Social**: Social media passwords

### Performance Optimization
1. **Multi-threading**: Enable for faster generation
2. **Thread Count**: Set based on your CPU cores
   - 4 cores: Use 4-6 threads
   - 8 cores: Use 6-8 threads
   - 16+ cores: Use 8-12 threads

### Configuration Management
1. **Save Config**: Click "Save Config" to store current settings
2. **Load Config**: Click "Load Config" to restore saved settings
3. **File Format**: JSON configuration files

### Analysis Tools
Enable **"Analyze Wordlist"** to get:
- Password strength distribution
- Common patterns detection
- Length distribution analysis
- Quality recommendations

---

# 💻 CLI USAGE GUIDE

## 🚀 Getting Started with CLI

### Basic Commands
```bash
# Interactive mode (recommended for beginners)
python wordlist.py

# Quick generation
python wordlist.py --min 8 --max 12 -c
```

### Help System
```bash
# Basic help
python wordlist.py --help

# Advanced examples
python wordlist.py --help-advanced
```

## 📚 Beginner CLI Guide

### Level 1: Basic Usage
```bash
# Simple wordlist with default settings
python wordlist.py

# Custom password length
python wordlist.py --min 6 --max 10

# Add numbers and years
python wordlist.py -r 999 -y 2000
```

### Level 2: Adding Features
```bash
# Include special characters
python wordlist.py -c

# Add leet permutations
python wordlist.py --leet

# Custom output file
python wordlist.py -x my_passwords.txt
```

### Level 3: Intermediate Usage
```bash
# Higher complexity
python wordlist.py -l 2 -c --leet

# Verbose mode (watch generation)
python wordlist.py -v -c --leet

# Combined features
python wordlist.py -l 2 --min 8 --max 16 -c --leet -x advanced.txt
```

## 🚀 Advanced CLI Guide

### Multi-Language Support
```bash
# Single language
python wordlist.py --languages hindi

# Multiple languages
python wordlist.py --languages hindi,arabic,chinese

# All European languages
python wordlist.py --languages european
```

### Pattern Templates
```bash
# Single template
python wordlist.py --templates common

# Multiple templates
python wordlist.py --templates common,corporate,personal

# Gaming focused
python wordlist.py --templates gaming --multithread
```

### Performance Optimization
```bash
# Multi-threaded generation
python wordlist.py --multithread --threads 8

# High-performance setup
python wordlist.py --multithread --threads 12 -l 4
```

### Configuration Management
```bash
# Save current setup
python wordlist.py --save-config corporate_setup.json

# Load saved setup
python wordlist.py --load-config corporate_setup.json

# Save and use immediately
python wordlist.py --save-config quick.json && python wordlist.py --load-config quick.json
```

### Analysis and Reporting
```bash
# Generate and analyze
python wordlist.py --analyze --templates common

# Analyze existing wordlist
python -c "from wordlist import main_ganerator; gen=main_ganerator(); gen.analyze_wordlist('passwords.txt')"
```

## 🎯 Specialized Use Cases

### Corporate Environment
```bash
python wordlist.py --templates corporate -l 3 -c --years 2010 --export corporate.txt
```

### Gaming Accounts
```bash
python wordlist.py --templates gaming --multithread --threads 6 --export gaming.txt
```

### Personal Passwords
```bash
python wordlist.py --templates personal -l 2 --years 1995 --export personal.txt
```

### Multi-language Targets
```bash
python wordlist.py --languages european,russian,chinese -l 4 --export international.txt
```

### Maximum Power Setup
```bash
python wordlist.py -l 5 --min 12 --max 20 -r 9999 -y 1990 -c --leet \
--templates common,corporate,gaming --languages hindi,chinese \
--multithread --threads 8 --analyze --export maximum.txt
```

## 🔧 Command Reference

### Basic Options
- `-l, --level`: Complexity (0-5)
- `--min`: Minimum length
- `--max`: Maximum length
- `-x, --export`: Output filename

### Content Options
- `-r, --num-range`: Number range (0 to N)
- `-y, --years`: Years from N to current
- `-c, --chars`: Add special characters
- `--leet`: Generate leet permutations

### Advanced Options
- `--languages`: Multi-language support
- `--templates`: Pattern templates
- `--multithread`: Enable multi-threading
- `--threads`: Thread count
- `--analyze`: Analyze wordlist

### Configuration
- `--save-config`: Save configuration
- `--load-config`: Load configuration
- `--help-advanced`: Show advanced examples

---

# 📊 Complexity Levels

| Level | Name | Description | Use Case |
|-------|------|-------------|----------|
| 0 | Simple | Basic permutations | Quick tests, low security |
| 1 | Average | More combinations | General purpose |
| 2 | Cyber Aware | Enhanced patterns | Security conscious |
| 3 | Paranoid | Advanced permutations | High security targets |
| 4 | Nerd | Complex combinations | Maximum coverage |
| 5 | Nuclear! | All permutations | Comprehensive testing |

---

# 🌍 Pattern Templates

## Common Templates
- `{name}{year}`, `{name}{number}`, `{name}{special}`
- `{name}{year}{number}`, `{year}{name}`, `{number}{name}`

## Corporate Templates
- `{company}{year}`, `Admin{year}`, `Password{year}`
- `{company}{department}{year}`, `{project}{year}`

## Personal Templates
- `{name}{birthdate}`, `{name}{pet}{year}`
- `{child}{name}{year}`, `{spouse}{name}{year}`

## Gaming Templates
- `{gamer}{tag}{year}`, `{game}{name}{year}`
- `{clan}{name}{year}`, `{character}{name}{year}`

## Social Templates
- `{name}{platform}{year}`, `{name}{handle}{year}`
- `{name}{follower}{year}`, `{name}{post}{year}`

---

# 💡 Pro Tips

## Performance Tips
- Use `--multithread` for large datasets
- Higher complexity levels take exponentially longer
- Combine templates for better coverage
- Save configurations for repeated use cases

## Quality Tips
- Always use `--analyze` to check wordlist quality
- Start with lower complexity levels and increase as needed
- Use specific templates rather than all templates
- Consider memory usage for very large wordlists

## Security Tips
- Use longer minimum lengths (12+ characters)
- Enable special characters and leet permutations
- Combine multiple complexity factors
- Test against known password policies

---

# 🔧 Troubleshooting

## Common Issues

### Memory Errors
```bash
# Reduce complexity or use multi-threading
python wordlist.py -l 2 --multithread --threads 4
```

### Slow Generation
```bash
# Enable multi-threading and reduce complexity
python wordlist.py --multithread --threads 8 -l 2
```

### Unicode Errors
```bash
# Specify language support explicitly
python wordlist.py --languages european
```

### Large File Sizes
```bash
# Use shorter password ranges
python wordlist.py --min 8 --max 10
```

## Getting Help
```bash
# Basic help
python wordlist.py --help

# Advanced examples
python wordlist.py --help-advanced

# GUI help
python gui.py  # Use intuitive interface
```

---

# 📈 Performance Benchmarks

## Single Thread vs Multi-thread
| Dataset Size | Single Thread | 4 Threads | 8 Threads |
|--------------|---------------|------------|------------|
| 10K passwords | 30s | 8s | 5s |
| 100K passwords | 5m | 1.5m | 45s |
| 1M passwords | 50m | 15m | 8m |

## Memory Usage
- Level 0-2: < 100MB
- Level 3-4: 100-500MB
- Level 5: 500MB-2GB

---

# 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

# 📄 License

This tool is for educational and authorized security testing purposes only. Users are responsible for ensuring compliance with applicable laws and regulations.

---

# 🆘 Support

- **GUI**: Use the intuitive interface for easy operation
- **CLI**: Run `python wordlist.py --help-advanced` for examples
- **Issues**: Report bugs via GitHub issues
- **Features**: Request features via GitHub discussions

---

## 🎉 Quick Start Summary

### For Beginners
```bash
# Install
pip install -r requirements.txt

# GUI (Easiest)
python gui.py

# CLI (Interactive)
python wordlist.py
```

### For Advanced Users
```bash
# Quick advanced setup
python wordlist.py -l 3 --min 10 --max 16 -c --leet --multithread --threads 8 --analyze

# Save and reuse
python wordlist.py --save-config my_setup.json
python wordlist.py --load-config my_setup.json
```

**Happy Password Hunting! 🔥**
