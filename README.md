# Auto-Commit Tool

A cross-platform GUI application that monitors Git repositories for changes and automatically commits and pushes them.

## Features

- GUI for adding/removing monitored folders
- Validates Git repos and remote origins
- Debounced commits to avoid spam
- System tray icon with quick actions
- Configurable commit messages (static or LLM-powered in future)

## Setup

1. Clone the repo
2. Install dependencies: pip install -e .
3. Run: auto-commit

## Requirements

- Python 3.11+
- Git
- PySide6, watchdog, GitPython

## License

MIT
