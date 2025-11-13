# Command Line Hero 🦸‍♂️

A feature-rich, text-based command-line interface built in Python. Experience a Unix-like shell with modern features like tab completion, reverse search, and command aliases!

## ✨ Features

### Core Commands
- **Navigation**: `cd`, `pwd`, `ls`, `tree`
- **File Operations**: `cat`, `touch`, `mkdir`, `rm`, `rmdir`, `mv`, `cp`
- **Text Processing**: `echo`, `head`, `tail`, `grep`, `wc`, `sort`, `diff`
- **Search**: `find`, `which`
- **System**: `clear`, `history`, `du`, `env`
- **Aliases**: `alias`, `unalias`

### Advanced Features
- ✅ **Tab Completion** - Press Tab to auto-complete commands and file paths
- ✅ **Reverse Search** - Press Ctrl+R to search command history
- ✅ **Command Aliases** - Create shortcuts (built-in: `ll`, `la`, `..`, `...`, `~`)
- ✅ **Colored Output** - Directories in blue, executables in green
- ✅ **Detailed Listings** - Use `ls -l` for permissions, sizes, and dates
- ✅ **Persistent History** - Command history saved to `~/.hero_history`

## 🚀 Quick Start

```bash
# Run the CLI
python3 cli.py

# Or make it executable
chmod +x cli.py
./cli.py
```

## 📖 Usage Examples

```bash
# Welcome screen appears
hero:~$ help              # Show all commands

# Navigate directories
hero:~$ ls -l             # Detailed listing
hero:~$ cd Documents      # Change directory
hero:Documents$ pwd       # Print working directory
hero:Documents$ ..        # Go back (alias for 'cd ..')

# File operations
hero:~$ touch test.txt    # Create file
hero:~$ echo "Hello" > test.txt  # (Note: redirection not yet implemented)
hero:~$ cat test.txt      # Display contents
hero:~$ cp test.txt backup.txt   # Copy file
hero:~$ mv backup.txt old.txt    # Rename/move file

# Text processing
hero:~$ head README.md 5  # Show first 5 lines
hero:~$ tail README.md 10 # Show last 10 lines
hero:~$ grep "Hero" README.md     # Search for text
hero:~$ wc README.md      # Count lines, words, chars
hero:~$ sort file.txt     # Sort file contents
hero:~$ diff file1.txt file2.txt  # Compare files

# Search and find
hero:~$ find ".py"        # Find files containing .py
hero:~$ tree              # Show directory tree
hero:~$ which ls          # Locate command
hero:~$ du .              # Disk usage

# Environment
hero:~$ env               # Show all variables
hero:~$ env PATH          # Show specific variable
hero:~$ env MY_VAR=value  # Set variable

# Aliases
hero:~$ alias             # Show all aliases
hero:~$ alias ll='ls -l'  # Create alias
hero:~$ ll                # Use alias
hero:~$ unalias ll        # Remove alias

# History
hero:~$ history           # Show recent commands
hero:~$ history 50        # Show last 50 commands
# Press Ctrl+R and type to search history!

# Exit
hero:~$ exit              # or 'quit' or Ctrl+D
```

## 🎨 Built-in Aliases

- `ll` → `ls -l` (detailed listing)
- `la` → `ls -la` (all files + details)
- `..` → `cd ..` (go up one directory)
- `...` → `cd ../..` (go up two directories)
- `~` → `cd ~` (go to home directory)

## 🎯 Tab Completion

Press **Tab** to auto-complete:
- Command names (e.g., `his` + Tab → `history`)
- File paths (e.g., `cat Re` + Tab → `cat README.md`)
- Directory names with trailing slash

## 🔍 Reverse Search (Ctrl+R)

Press **Ctrl+R** and start typing to search through your command history. This is a built-in readline feature that works automatically!

## 🧪 Running Tests

```bash
# Setup virtual environment (optional)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install pytest
pip install pytest

# Run tests
pytest tests/ -v
```

## 📝 Command Reference

### Navigation Commands
- `cd [dir]` - Change directory (supports `~` for home)
- `pwd` - Print working directory
- `ls [-l] [-a] [path]` - List directory contents
  - `-l` = detailed format
  - `-a` = show hidden files
- `tree [path] [depth]` - Show directory tree structure

### File Operations
- `cat <file>` - Display file contents
- `touch <file>` - Create or update file
- `mkdir <dir>` - Create directory
- `rm <file>` - Remove file
- `rmdir [-r] <dir>` - Remove directory
  - `-r` = recursive
- `mv <src> <dst>` - Move or rename
- `cp <src> <dst>` - Copy file or directory

### Text Processing
- `echo <text>` - Print text
- `head <file> [n]` - Show first n lines (default: 10)
- `tail <file> [n]` - Show last n lines (default: 10)
- `grep <pattern> <file>` - Search for pattern
- `wc <file>` - Count lines, words, characters
- `sort <file>` - Sort lines alphabetically
- `diff <file1> <file2>` - Compare two files

### Search & System
- `find <pattern> [path]` - Find files by name
- `which <command>` - Locate command
- `du [path]` - Show disk usage
- `env [VAR] [VAR=value]` - Environment variables
- `clear` - Clear screen
- `history [n]` - Show command history

### Aliases
- `alias` - List all aliases
- `alias name='command'` - Create alias
- `unalias name` - Remove alias

## 🎨 Color Scheme

- **Directories**: Blue and bold with trailing `/`
- **Executables**: Green with trailing `*`
- **Regular files**: Default color
- **Prompt**: Green "hero" with blue path
- **Grep matches**: Green filename, cyan line numbers
- **Errors**: Red text

## 🔧 Configuration

History is automatically saved to `~/.hero_history` and persists across sessions.

## 🚧 Future Enhancements

Want to contribute? Here are some ideas:
- Output redirection (`>`, `>>`)
- Pipes (`|`)
- Background jobs (`&`)
- Command chaining (`&&`, `||`, `;`)
- More advanced wildcards (`*`, `?`, `[]`)
- Configuration file (`~/.herorc`)

## 📄 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

This is a learning project! Feel free to fork and add your own commands.

---

**Enjoy your Command Line Hero journey! 🚀**
