# Command Line Hero 🦸‍♂️

> **A feature-rich command-line interface built in Python**  
> Experience a Unix-like shell with modern features like tab completion, reverse search, command aliases, and text editors!

---

## 🚀 Getting Started

Run Command Line Hero from your terminal:

```bash
python3 cli.py
```

You'll be greeted with an interactive prompt:

```
🚀 Welcome to Command Line Hero!
Type 'help' for available commands, 'exit' to quit.

hero:~$ 
```

The prompt shows your current location relative to where you started. Type `help` to see all available commands.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Tab Completion** | Press `Tab` to auto-complete commands and file paths |
| **Reverse Search** | Press `Ctrl+R` to search through command history |
| **Command Aliases** | Create shortcuts for frequently used commands |
| **Colored Output** | Visual distinction: directories (blue), executables (green) |
| **Persistent History** | Commands saved to `~/.hero_history` across sessions |
| **Text Editors** | Launch vim, nano, or your preferred `$EDITOR` directly |

---

## 📖 Command Reference

### 🧭 Navigation

Navigate through your filesystem with ease:

| Command | Description | Example |
|---------|-------------|---------|
| `cd [dir]` | Change to a directory | `cd Documents` |
| `pwd` | Print working directory | `pwd` |
| `ls [options] [path]` | List directory contents | `ls -la` |
| `tree [path] [depth]` | Display directory tree | `tree . 2` |

**Options for `ls`:**
- `-l` — Detailed format with permissions, size, and date
- `-a` — Show hidden files (starting with `.`)
- `-la` — Combine both options

**Example:**
```bash
hero:~$ ls -l
drwxr-xr-x     4096 Nov 27 10:30 Documents/
-rw-r--r--     1234 Nov 27 09:15 README.md
-rwxr-xr-x     8192 Nov 26 14:20 script.py*
```

---

### 📁 File Operations

Create, view, move, copy, and delete files:

| Command | Description | Example |
|---------|-------------|---------|
| `cat <file>` | Display file contents | `cat config.txt` |
| `touch <file>` | Create or update file timestamp | `touch newfile.txt` |
| `mkdir <dir>` | Create directory | `mkdir myproject` |
| `rm <file>` | Remove file | `rm oldfile.txt` |
| `rmdir [-r] <dir>` | Remove directory | `rmdir -r oldfolder` |
| `mv <src> <dst>` | Move or rename file | `mv old.txt new.txt` |
| `cp <src> <dst>` | Copy file or directory | `cp file.txt backup.txt` |

**Options:**
- `rmdir -r` — Remove directory recursively (including contents)

**Example:**
```bash
hero:~$ touch notes.txt
hero:~$ mkdir projects
hero:~$ mv notes.txt projects/
Moved: notes.txt -> projects/
```

---

### ✏️ Text Editors

Edit files directly from Command Line Hero:

| Command | Description | Example |
|---------|-------------|---------|
| `edit <file>` | Open file in your editor (respects `$EDITOR`) | `edit config.txt` |
| `vim <file>` | Open file in Vim | `vim script.py` |
| `nano <file>` | Open file in Nano | `nano README.md` |

**How it works:**
- `edit` uses your system's `$EDITOR` environment variable
- If `$EDITOR` is not set, it defaults to `vim`
- `vim` and `nano` are direct shortcuts to those editors
- The CLI blocks while you're editing and resumes when you exit the editor

**Example:**
```bash
hero:~$ edit myfile.txt
# Opens your default editor
# Make your changes and save
# When you exit, you're back to the hero prompt
```

---

### 📝 Text Processing

View, search, and analyze text files:

| Command | Description | Example |
|---------|-------------|---------|
| `echo <text>` | Print text to screen | `echo Hello World` |
| `head <file> [n]` | Show first n lines (default: 10) | `head log.txt 5` |
| `tail <file> [n]` | Show last n lines (default: 10) | `tail log.txt 20` |
| `grep <pattern> <file>` | Search for text pattern | `grep "error" log.txt` |
| `wc <file>` | Count lines, words, characters | `wc README.md` |
| `sort <file>` | Sort lines alphabetically | `sort names.txt` |
| `diff <file1> <file2>` | Compare two files | `diff old.py new.py` |

**Example:**
```bash
hero:~$ grep "TODO" script.py
script.py:15:# TODO: Add error handling
script.py:42:# TODO: Optimize this loop

hero:~$ wc README.md
      45      320     2048 README.md
```

**Understanding `wc` output:**
```
lines    words    chars    filename
```

---

### 🔍 Search & Discovery

Find files and commands:

| Command | Description | Example |
|---------|-------------|---------|
| `find <pattern> [path]` | Find files by name | `find ".py" src/` |
| `which <command>` | Locate where a command is | `which ls` |
| `du [path]` | Show disk usage | `du Documents/` |

**Example:**
```bash
hero:~$ find "config"
./config.json
./backup/old_config.json
./settings/user_config.yaml

hero:~$ which cd
cd: built-in command
```

---

### ⚙️ System & Environment

Manage your shell environment:

| Command | Description | Example |
|---------|-------------|---------|
| `env` | Show all environment variables | `env` |
| `env <VAR>` | Show specific variable | `env PATH` |
| `env VAR=value` | Set environment variable | `env EDITOR=nano` |
| `clear` | Clear the screen | `clear` |
| `history [n]` | Show command history | `history 50` |
| `help` | Display all commands | `help` |
| `exit` / `quit` | Exit Command Line Hero | `exit` |

**Example:**
```bash
hero:~$ env EDITOR=nano
Set: EDITOR=nano

hero:~$ history 5
  96 ls -la
  97 cd projects
  98 grep "error" log.txt
  99 env EDITOR=nano
 100 history 5
```

---

### 🔗 Aliases

Create shortcuts for frequently used commands:

| Command | Description | Example |
|---------|-------------|---------|
| `alias` | List all aliases | `alias` |
| `alias name='cmd'` | Create alias | `alias ll='ls -l'` |
| `unalias <name>` | Remove alias | `unalias ll` |

**Built-in Aliases:**

| Alias | Expands To | Description |
|-------|------------|-------------|
| `ll` | `ls -l` | Detailed file listing |
| `la` | `ls -la` | All files with details |
| `..` | `cd ..` | Go up one directory |
| `...` | `cd ../..` | Go up two directories |
| `~` | `cd ~` | Go to home directory |

**Example:**
```bash
hero:~$ alias gp='grep -n "pattern"'
Alias created: gp='grep -n "pattern"'

hero:~$ gp file.txt
# Now uses: grep -n "pattern" file.txt
```

---

## 🎨 Visual Indicators

Command Line Hero uses color-coding for better readability:

| Item | Color | Example |
|------|-------|---------|
| Directories | **Blue + Bold** | `Documents/` |
| Executables | **Green** | `script.py*` |
| Regular Files | Default | `file.txt` |
| Prompt | Green (hero) + Blue (path) | `hero:~/projects$` |
| Error Messages | **Red** | Error text |
| Grep Matches | Green (file) + Cyan (line #) | `file.txt:42:match` |

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` | Auto-complete commands and file paths |
| `Ctrl+R` | Reverse search through command history |
| `Ctrl+D` | Exit (same as `exit` command) |
| `Ctrl+C` | Cancel current input |
| `Up/Down Arrow` | Navigate through command history |

**Tab Completion Examples:**
```bash
hero:~$ his[Tab]
hero:~$ history

hero:~$ cd Doc[Tab]
hero:~$ cd Documents/
```

**Reverse Search (`Ctrl+R`):**
1. Press `Ctrl+R`
2. Start typing part of a previous command
3. Press `Ctrl+R` again to cycle through matches
4. Press `Enter` to execute, or `Esc` to cancel

---

## 🔧 How It Works

### Command Processing

1. **Input:** You type a command at the prompt
2. **Alias Expansion:** Built-in and custom aliases are expanded
3. **Parsing:** The command is split into command + arguments
4. **Execution:** The appropriate function is called
5. **History:** The command is saved to history
6. **Persistence:** On exit, history is saved to `~/.hero_history`

### Tab Completion

- Uses Python's `readline` library for intelligent completion
- Completes commands when typing at the start of a line
- Completes file and directory names for arguments
- Automatically adds `/` to directories

### Color Scheme

Command Line Hero uses ANSI escape codes for terminal colors:
- Colors work on Linux, macOS, and modern Windows terminals
- File types are detected using `os.stat()` and file permissions
- Directories are identified with `os.path.isdir()`
- Executables are identified by checking the execute bit

### Editor Integration

When you use `edit`, `vim`, or `nano`:
1. The command spawns a subprocess using `subprocess.call()`
2. The subprocess inherits the terminal's stdin/stdout/stderr
3. Command Line Hero blocks (waits) until the editor exits
4. You're returned to the hero prompt after saving/exiting

This allows full interactivity with text editors without leaving the hero shell.

---

## 📚 Usage Examples

### Example 1: Basic File Management
```bash
hero:~$ mkdir myproject
Created: myproject

hero:~$ cd myproject
hero:~/myproject$ touch main.py README.md

hero:~/myproject$ ls
main.py  README.md

hero:~/myproject$ edit main.py
# Opens editor, write code, save & exit

hero:~/myproject$ cat main.py
print("Hello, Command Line Hero!")
```

### Example 2: Finding and Searching
```bash
hero:~$ find ".txt"
./notes.txt
./docs/readme.txt
./archive/old.txt

hero:~$ grep "important" notes.txt
notes.txt:5:This is important information
notes.txt:18:Another important note

hero:~$ wc notes.txt
     42     256    1847 notes.txt
```

### Example 3: Directory Navigation
```bash
hero:~$ ls
Documents/  Downloads/  Pictures/

hero:~$ cd Documents
hero:~/Documents$ pwd
/home/user/Documents

hero:~/Documents$ ..
hero:~$ pwd
/home/user
```

### Example 4: Creating Aliases
```bash
hero:~$ alias projects='cd ~/projects'
Alias created: projects='cd ~/projects'

hero:~$ projects
hero:~/projects$ pwd
/home/user/projects

hero:~/projects$ alias ll
ll='ls -l'
```

### Example 5: Text Analysis
```bash
hero:~$ head README.md 3
# Command Line Hero
A feature-rich CLI
Built in Python

hero:~$ tail README.md 2
---
Enjoy your journey! 🚀

hero:~$ wc -l *.py
     45 main.py
    123 utils.py
    289 core.py
```

---

## 💡 Tips & Tricks

1. **Quick Navigation:**
   - Use `..` to go up one directory
   - Use `...` to go up two directories
   - Use `~` to jump to home directory

2. **Efficient Listing:**
   - `ll` for detailed view
   - `la` to see hidden files
   - `tree` for visual structure

3. **Search History:**
   - `Ctrl+R` is faster than scrolling through `history`
   - Type a few letters and it finds matches instantly

4. **Custom Aliases:**
   - Create aliases for your most-used commands
   - Save time with short names like `gp` for `grep`

5. **Editor Configuration:**
   - Set `$EDITOR` in your shell: `export EDITOR=nano`
   - Then `edit` will always use your preferred editor

---

**Happy commanding! 🚀**
