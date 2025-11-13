#!/usr/bin/env python3
"""Command Line Hero - A feature-rich text-based CLI."""
from command_hero import CommandHero


def main():
    print("🚀 Welcome to Command Line Hero!")
    print("Type 'help' for available commands, 'exit' to quit.\n")
    
    hero = CommandHero()
    try:
        hero.cmdloop()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting Command Line Hero. Goodbye!")


if __name__ == "__main__":
    main()
