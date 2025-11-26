import os
import sys
import shlex
import subprocess
import readline
import glob
import stat
import datetime
import shutil
import difflib
from typing import Callable, Dict, List, Optional
from pathlib import Path


class CommandHero:
    """Feature-rich command-line interface with tab completion and aliases."""

    # ANSI color codes
    COLORS = {
        'reset': '\033[0m',
        'blue': '\033[94m',
        'green': '\033[92m',
        'cyan': '\033[96m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'magenta': '\033[95m',
        'bold': '\033[1m',
        'dim': '\033[2m',
    }

    def __init__(self, base_dir: str = None):
        """Create a CommandHero CLI instance."""
        self.base_dir = base_dir or os.path.abspath(os.getcwd())
        self._running = True
        self._history: List[str] = []
        self._env_vars: Dict[str, str] = {}
        
        # Built-in command aliases
        self._aliases: Dict[str, str] = {
            "ll": "ls -l",
            "la": "ls -la",
            "..": "cd ..",
            "...": "cd ../..",
            "~": "cd ~",
        }
        
        # Command registry
        self._commands: Dict[str, Callable[[List[str]], None]] = {
            "help": self._help,
            "ls": self._ls,
            "pwd": self._pwd,
            "cd": self._cd,
            "cat": self._cat,
            "echo": self._echo,
            "clear": self._clear,
            "history": self._history_cmd,
            "touch": self._touch,
            "rm": self._rm,
            "mkdir": self._mkdir,
            "rmdir": self._rmdir,
            "mv": self._mv,
            "cp": self._cp,
            "head": self._head,
            "tail": self._tail,
            "grep": self._grep,
            "wc": self._wc,
            "find": self._find,
            "tree": self._tree,
            "du": self._du,
            "diff": self._diff,
            "edit": self._edit,
            "vim": self._vim,
            "nano": self._nano,
            "sort": self._sort,
            "env": self._env,
            "which": self._which,
            "alias": self._alias_cmd,
            "unalias": self._unalias,
            "exit": self._exit,
            "quit": self._exit,
        }
        
        # Setup readline for tab completion and history
        self._setup_readline()

    def _setup_readline(self):
        """Configure readline for tab completion and reverse search."""
        try:
            # Set history length
            readline.set_history_length(1000)
            
            # Tab completion
            readline.set_completer(self._completer)
            readline.parse_and_bind("tab: complete")
            
            # Reverse search (Ctrl+R) - already built into readline
            # Set completer delimiters
            readline.set_completer_delims(' \t\n;')
            
            # Try to load history from file
            history_file = os.path.expanduser("~/.hero_history")
            if os.path.exists(history_file):
                readline.read_history_file(history_file)
        except Exception:
            pass  # readline not available on some systems

    def _save_history(self):
        """Save command history to file."""
        try:
            history_file = os.path.expanduser("~/.hero_history")
            readline.write_history_file(history_file)
        except Exception:
            pass

    def cmdloop(self):
        """Main command loop."""
        while self._running:
            try:
                cwd = os.path.relpath(os.getcwd(), self.base_dir)
                if cwd == ".":
                    cwd = "~"
                
                prompt = (
                    f"{self.COLORS['green']}{self.COLORS['bold']}hero"
                    f"{self.COLORS['reset']}:{self.COLORS['blue']}{cwd}"
                    f"{self.COLORS['reset']}$ "
                )
                
                line = input(prompt)
            except EOFError:
                print()
                break
            
            line = line.strip()
            if not line:
                continue
            
            # Save to history
            self._history.append(line)
            
            # Expand aliases
            line = self._expand_alias(line)
            
            # Parse and execute
            try:
                parts = shlex.split(line)
                if parts:
                    cmd, args = parts[0], parts[1:]
                    self.run_command(cmd, args)
            except ValueError as e:
                print(f"Parse error: {e}")
            except Exception as e:
                print(f"Error: {e}")
        
        self._save_history()

    def run_command(self, cmd: str, args: List[str]) -> None:
        """Execute a command."""
        fn = self._commands.get(cmd)
        if fn:
            try:
                fn(args)
            except Exception as e:
                print(f"{self.COLORS['red']}Error: {e}{self.COLORS['reset']}")
        else:
            print(f"{self.COLORS['red']}Unknown command: {cmd}{self.COLORS['reset']}")
            print(f"Type 'help' for available commands.")

    def _expand_alias(self, line: str) -> str:
        """Expand command aliases."""
        parts = line.split(None, 1)
        if not parts:
            return line
        cmd = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        if cmd in self._aliases:
            expanded = self._aliases[cmd]
            return f"{expanded} {rest}" if rest else expanded
        return line

    def _completer(self, text: str, state: int) -> Optional[str]:
        """Tab completion handler."""
        line = readline.get_line_buffer()
        parts = line.split()
        
        # Complete commands if at the beginning
        if not parts or (len(parts) == 1 and not line.endswith(" ")):
            commands = [cmd for cmd in self._commands.keys() if cmd.startswith(text)]
            commands += [alias for alias in self._aliases.keys() if alias.startswith(text)]
            commands = sorted(set(commands))
            return commands[state] if state < len(commands) else None
        
        # Complete file/directory names
        if text:
            matches = glob.glob(text + "*")
        else:
            matches = glob.glob("*")
        
        # Add trailing slash for directories
        matches = [m + "/" if os.path.isdir(m) else m for m in matches]
        return matches[state] if state < len(matches) else None

    # ===== COMMAND IMPLEMENTATIONS =====

    def _help(self, args: List[str]):
        """Show all available commands."""
        print(f"\n{self.COLORS['bold']}Available Commands:{self.COLORS['reset']}\n")
        
        categories = {
            "Navigation": ["cd", "pwd", "ls", "tree"],
            "File Operations": ["cat", "touch", "mkdir", "rm", "rmdir", "mv", "cp", "edit"],
            "Text Processing": ["echo", "head", "tail", "grep", "wc", "sort", "diff"],
            "Search": ["find", "which"],
            "System": ["clear", "history", "du", "env"],
            "Aliases": ["alias", "unalias"],
            "Control": ["help", "exit", "quit"],
        }
        
        for category, cmds in categories.items():
            print(f"{self.COLORS['cyan']}{category}:{self.COLORS['reset']}")
            for cmd in cmds:
                if cmd in self._commands:
                    print(f"  {self.COLORS['green']}{cmd}{self.COLORS['reset']}")
            print()
        
        print(f"{self.COLORS['yellow']}Tips:{self.COLORS['reset']}")
        print(f"  • Press {self.COLORS['bold']}Tab{self.COLORS['reset']} for auto-completion")
        print(f"  • Press {self.COLORS['bold']}Ctrl+R{self.COLORS['reset']} for reverse search")
        print(f"  • Use {self.COLORS['bold']}alias{self.COLORS['reset']} to create shortcuts")
        print(f"  • Built-in aliases: ll, la, .., ..., ~\n")

    def _ls(self, args: List[str]):
        """List directory contents with colors."""
        long_format = "-l" in args or "-la" in args
        show_hidden = "-a" in args or "-la" in args
        args = [a for a in args if not a.startswith("-")]
        path = args[0] if args else "."
        
        try:
            entries = os.listdir(path)
            if not show_hidden:
                entries = [e for e in entries if not e.startswith(".")]
            entries.sort()
            
            if long_format:
                # Detailed listing
                for name in entries:
                    full_path = os.path.join(path, name)
                    try:
                        st = os.stat(full_path)
                        perms = stat.filemode(st.st_mode)
                        size = st.st_size
                        mtime = datetime.datetime.fromtimestamp(st.st_mtime).strftime('%b %d %H:%M')
                        
                        # Colorize name
                        if os.path.isdir(full_path):
                            colored_name = f"{self.COLORS['blue']}{self.COLORS['bold']}{name}/{self.COLORS['reset']}"
                        elif os.access(full_path, os.X_OK):
                            colored_name = f"{self.COLORS['green']}{name}*{self.COLORS['reset']}"
                        else:
                            colored_name = name
                        
                        print(f"{perms} {size:>8} {mtime} {colored_name}")
                    except Exception:
                        print(name)
            else:
                # Simple listing with colors
                for name in entries:
                    full_path = os.path.join(path, name)
                    if os.path.isdir(full_path):
                        print(f"{self.COLORS['blue']}{self.COLORS['bold']}{name}/{self.COLORS['reset']}")
                    elif os.access(full_path, os.X_OK):
                        print(f"{self.COLORS['green']}{name}*{self.COLORS['reset']}")
                    else:
                        print(name)
        except FileNotFoundError:
            print(f"{self.COLORS['red']}No such directory: {path}{self.COLORS['reset']}")
        except PermissionError:
            print(f"{self.COLORS['red']}Permission denied: {path}{self.COLORS['reset']}")

    def _pwd(self, args: List[str]):
        """Print working directory."""
        print(os.getcwd())

    def _cd(self, args: List[str]):
        """Change directory."""
        if not args or args[0] == "~":
            target = os.path.expanduser("~")
        else:
            target = args[0]
        
        try:
            os.chdir(os.path.expanduser(target))
        except FileNotFoundError:
            print(f"{self.COLORS['red']}No such directory: {target}{self.COLORS['reset']}")
        except PermissionError:
            print(f"{self.COLORS['red']}Permission denied: {target}{self.COLORS['reset']}")

    def _cat(self, args: List[str]):
        """Display file contents."""
        if not args:
            print("Usage: cat <file>")
            return
        
        for filepath in args:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    print(f.read(), end="")
            except FileNotFoundError:
                print(f"{self.COLORS['red']}No such file: {filepath}{self.COLORS['reset']}")
            except PermissionError:
                print(f"{self.COLORS['red']}Permission denied: {filepath}{self.COLORS['reset']}")

    def _edit(self, args: List[str]):
        """Open a file in the user's editor (respects $EDITOR)."""
        # Determine editor: explicit arg, $EDITOR, fallback to vim
        editor = os.environ.get("EDITOR") or "vim"
        cmd = [editor]
        if args:
            cmd += args

        try:
            # Launch the editor, inheriting stdio so interactive editors work
            subprocess.call(cmd)
        except FileNotFoundError:
            print(f"{self.COLORS['red']}Editor not found: {cmd[0]}{self.COLORS['reset']}")
        except Exception as e:
            print(f"{self.COLORS['red']}Failed to launch editor: {e}{self.COLORS['reset']}")

    def _vim(self, args: List[str]):
        """Shortcut to open vim (or fall back if not present)."""
        cmd = ["vim"] + args
        try:
            subprocess.call(cmd)
        except FileNotFoundError:
            print(f"{self.COLORS['red']}vim not found{self.COLORS['reset']}")
        except Exception as e:
            print(f"{self.COLORS['red']}Failed to launch vim: {e}{self.COLORS['reset']}")

    def _nano(self, args: List[str]):
        """Shortcut to open nano."""
        cmd = ["nano"] + args
        try:
            subprocess.call(cmd)
        except FileNotFoundError:
            print(f"{self.COLORS['red']}nano not found{self.COLORS['reset']}")
        except Exception as e:
            print(f"{self.COLORS['red']}Failed to launch nano: {e}{self.COLORS['reset']}")

    def _echo(self, args: List[str]):
        """Print text to stdout."""
        print(" ".join(args))

    def _clear(self, args: List[str]):
        """Clear the terminal screen."""
        os.system("clear" if os.name != "nt" else "cls")

    def _history_cmd(self, args: List[str]):
        """Show command history."""
        n = int(args[0]) if args and args[0].isdigit() else 200
        recent = self._history[-n:]
        for i, cmd in enumerate(recent, start=len(self._history) - len(recent) + 1):
            print(f"{self.COLORS['dim']}{i:>4}{self.COLORS['reset']} {cmd}")

    def _touch(self, args: List[str]):
        """Create or update file timestamp."""
        if not args:
            print("Usage: touch <file>")
            return
        
        for filepath in args:
            try:
                Path(filepath).touch()
            except Exception as e:
                print(f"{self.COLORS['red']}Failed to touch {filepath}: {e}{self.COLORS['reset']}")

    def _rm(self, args: List[str]):
        """Remove files."""
        if not args:
            print("Usage: rm <file> [file...]")
            return
        
        for filepath in args:
            try:
                if os.path.isdir(filepath):
                    print(f"{self.COLORS['yellow']}Skipping directory {filepath} (use rmdir){self.COLORS['reset']}")
                else:
                    os.remove(filepath)
                    print(f"Removed: {filepath}")
            except FileNotFoundError:
                print(f"{self.COLORS['red']}No such file: {filepath}{self.COLORS['reset']}")
            except Exception as e:
                print(f"{self.COLORS['red']}Failed to remove {filepath}: {e}{self.COLORS['reset']}")

    def _mkdir(self, args: List[str]):
        """Create directories."""
        if not args:
            print("Usage: mkdir <dir> [dir...]")
            return
        
        for dirpath in args:
            try:
                os.makedirs(dirpath, exist_ok=True)
                print(f"Created: {dirpath}")
            except Exception as e:
                print(f"{self.COLORS['red']}Failed to create {dirpath}: {e}{self.COLORS['reset']}")

    def _rmdir(self, args: List[str]):
        """Remove directories."""
        if not args:
            print("Usage: rmdir <dir> [dir...] [-r for recursive]")
            return
        
        recursive = "-r" in args
        dirs = [a for a in args if not a.startswith("-")]
        
        for dirpath in dirs:
            try:
                if recursive:
                    shutil.rmtree(dirpath)
                else:
                    os.rmdir(dirpath)
                print(f"Removed: {dirpath}")
            except FileNotFoundError:
                print(f"{self.COLORS['red']}No such directory: {dirpath}{self.COLORS['reset']}")
            except OSError as e:
                print(f"{self.COLORS['red']}Failed to remove {dirpath}: {e}{self.COLORS['reset']}")

    def _mv(self, args: List[str]):
        """Move or rename files."""
        if len(args) < 2:
            print("Usage: mv <source> <dest>")
            return
        
        src, dst = args[0], args[1]
        try:
            shutil.move(src, dst)
            print(f"Moved: {src} -> {dst}")
        except Exception as e:
            print(f"{self.COLORS['red']}Failed to move: {e}{self.COLORS['reset']}")

    def _cp(self, args: List[str]):
        """Copy files or directories."""
        if len(args) < 2:
            print("Usage: cp <source> <dest>")
            return
        
        src, dst = args[0], args[1]
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            print(f"Copied: {src} -> {dst}")
        except Exception as e:
            print(f"{self.COLORS['red']}Failed to copy: {e}{self.COLORS['reset']}")

    def _head(self, args: List[str]):
        """Show first N lines of a file."""
        if not args:
            print("Usage: head <file> [n]")
            return
        
        filepath = args[0]
        n = int(args[1]) if len(args) > 1 else 10
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    if i >= n:
                        break
                    print(line, end="")
        except FileNotFoundError:
            print(f"{self.COLORS['red']}No such file: {filepath}{self.COLORS['reset']}")

    def _tail(self, args: List[str]):
        """Show last N lines of a file."""
        if not args:
            print("Usage: tail <file> [n]")
            return
        
        filepath = args[0]
        n = int(args[1]) if len(args) > 1 else 10
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[-n:]:
                    print(line, end="")
        except FileNotFoundError:
            print(f"{self.COLORS['red']}No such file: {filepath}{self.COLORS['reset']}")

    def _grep(self, args: List[str]):
        """Search for pattern in files."""
        if len(args) < 2:
            print("Usage: grep <pattern> <file> [file...]")
            return
        
        pattern = args[0]
        files = args[1:]
        
        for filepath in files:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f, start=1):
                        if pattern in line:
                            print(f"{self.COLORS['green']}{filepath}{self.COLORS['reset']}:"
                                  f"{self.COLORS['cyan']}{i}{self.COLORS['reset']}:"
                                  f"{line.rstrip()}")
            except FileNotFoundError:
                print(f"{self.COLORS['red']}No such file: {filepath}{self.COLORS['reset']}")

    def _wc(self, args: List[str]):
        """Count lines, words, and characters in files."""
        if not args:
            print("Usage: wc <file> [file...]")
            return
        
        for filepath in args:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.count('\n')
                    words = len(content.split())
                    chars = len(content)
                    print(f"{lines:>8} {words:>8} {chars:>8} {filepath}")
            except FileNotFoundError:
                print(f"{self.COLORS['red']}No such file: {filepath}{self.COLORS['reset']}")

    def _find(self, args: List[str]):
        """Find files by name pattern."""
        if not args:
            print("Usage: find <pattern> [path]")
            return
        
        pattern = args[0]
        start_path = args[1] if len(args) > 1 else "."
        
        try:
            for root, dirs, files in os.walk(start_path):
                for name in files + dirs:
                    if pattern in name:
                        full_path = os.path.join(root, name)
                        if os.path.isdir(full_path):
                            print(f"{self.COLORS['blue']}{full_path}/{self.COLORS['reset']}")
                        else:
                            print(full_path)
        except Exception as e:
            print(f"{self.COLORS['red']}Error: {e}{self.COLORS['reset']}")

    def _tree(self, args: List[str]):
        """Display directory tree structure."""
        path = args[0] if args else "."
        max_depth = int(args[1]) if len(args) > 1 else 3
        
        def print_tree(directory, prefix="", depth=0):
            if depth > max_depth:
                return
            
            try:
                entries = sorted(os.listdir(directory))
                entries = [e for e in entries if not e.startswith(".")]
                
                for i, entry in enumerate(entries):
                    full_path = os.path.join(directory, entry)
                    is_last = i == len(entries) - 1
                    connector = "└── " if is_last else "├── "
                    
                    if os.path.isdir(full_path):
                        print(f"{prefix}{connector}{self.COLORS['blue']}{entry}/{self.COLORS['reset']}")
                        extension = "    " if is_last else "│   "
                        print_tree(full_path, prefix + extension, depth + 1)
                    else:
                        print(f"{prefix}{connector}{entry}")
            except PermissionError:
                print(f"{prefix}[Permission Denied]")
        
        print(f"{self.COLORS['blue']}{path}/{self.COLORS['reset']}")
        print_tree(path)

    def _du(self, args: List[str]):
        """Show disk usage of directories."""
        path = args[0] if args else "."
        
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except:
                        pass
            
            # Convert to human-readable format
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if total_size < 1024.0:
                    print(f"{total_size:.1f}{unit}\t{path}")
                    break
                total_size /= 1024.0
        except Exception as e:
            print(f"{self.COLORS['red']}Error: {e}{self.COLORS['reset']}")

    def _diff(self, args: List[str]):
        """Compare two files line by line."""
        if len(args) < 2:
            print("Usage: diff <file1> <file2>")
            return
        
        file1, file2 = args[0], args[1]
        
        try:
            with open(file1, "r") as f1, open(file2, "r") as f2:
                lines1 = f1.readlines()
                lines2 = f2.readlines()
            
            diff = difflib.unified_diff(lines1, lines2, fromfile=file1, tofile=file2, lineterm='')
            
            for line in diff:
                if line.startswith('+'):
                    print(f"{self.COLORS['green']}{line}{self.COLORS['reset']}")
                elif line.startswith('-'):
                    print(f"{self.COLORS['red']}{line}{self.COLORS['reset']}")
                elif line.startswith('@'):
                    print(f"{self.COLORS['cyan']}{line}{self.COLORS['reset']}")
                else:
                    print(line)
        except FileNotFoundError as e:
            print(f"{self.COLORS['red']}File not found: {e}{self.COLORS['reset']}")

    def _sort(self, args: List[str]):
        """Sort lines in a file."""
        if not args:
            print("Usage: sort <file>")
            return
        
        filepath = args[0]
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            for line in sorted(lines):
                print(line, end="")
        except FileNotFoundError:
            print(f"{self.COLORS['red']}No such file: {filepath}{self.COLORS['reset']}")

    def _env(self, args: List[str]):
        """Show or set environment variables."""
        if not args:
            # Show all environment variables
            for key, value in sorted(os.environ.items()):
                print(f"{self.COLORS['cyan']}{key}{self.COLORS['reset']}={value}")
        elif "=" in args[0]:
            # Set environment variable
            key, value = args[0].split("=", 1)
            os.environ[key] = value
            self._env_vars[key] = value
            print(f"Set: {key}={value}")
        else:
            # Show specific variable
            key = args[0]
            value = os.environ.get(key)
            if value:
                print(f"{key}={value}")
            else:
                print(f"{self.COLORS['red']}Variable not found: {key}{self.COLORS['reset']}")

    def _which(self, args: List[str]):
        """Locate a command."""
        if not args:
            print("Usage: which <command>")
            return
        
        cmd = args[0]
        
        # Check if it's a built-in command
        if cmd in self._commands:
            print(f"{cmd}: built-in command")
            return
        
        # Check if it's an alias
        if cmd in self._aliases:
            print(f"{cmd}: aliased to '{self._aliases[cmd]}'")
            return
        
        # Check PATH
        path_dirs = os.environ.get("PATH", "").split(os.pathsep)
        for directory in path_dirs:
            full_path = os.path.join(directory, cmd)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                print(full_path)
                return
        
        print(f"{self.COLORS['red']}{cmd} not found{self.COLORS['reset']}")

    def _alias_cmd(self, args: List[str]):
        """Create or show command aliases."""
        if not args:
            # Show all aliases
            for name, cmd in sorted(self._aliases.items()):
                print(f"{self.COLORS['cyan']}{name}{self.COLORS['reset']}='{cmd}'")
        elif "=" in args[0]:
            # Create alias
            name, cmd = args[0].split("=", 1)
            self._aliases[name] = cmd.strip("'\"")
            print(f"Alias created: {name}='{self._aliases[name]}'")
        else:
            # Show specific alias
            name = args[0]
            if name in self._aliases:
                print(f"{name}='{self._aliases[name]}'")
            else:
                print(f"{self.COLORS['red']}Alias not found: {name}{self.COLORS['reset']}")

    def _unalias(self, args: List[str]):
        """Remove command aliases."""
        if not args:
            print("Usage: unalias <name>")
            return
        
        name = args[0]
        if name in self._aliases:
            del self._aliases[name]
            print(f"Removed alias: {name}")
        else:
            print(f"{self.COLORS['red']}Alias not found: {name}{self.COLORS['reset']}")

    def _exit(self, args: List[str]):
        """Exit the CLI."""
        self._running = False
        print(f"\n{self.COLORS['cyan']}Goodbye! 👋{self.COLORS['reset']}")
