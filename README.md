# taskboard

A simple local task-list CLI with SQLite persistence. No dependencies, no web UI, no network, no user management.

## Usage

Run commands using:

    python -m taskboard --database PATH <command> [args]

- `--database PATH` (optional): Path to SQLite database file (default: `tasks.sqlite3` in current directory)
- Commands:
    - `add TITLE` — Add a new task with the given TITLE
    - `list` — List all tasks
    - `complete ID` — Mark the task with the given ID as completed

All commands print a single JSON value to stdout on success (exit 0). Errors print a JSON object to stderr and exit 2. Data persists across runs and separate databases are isolated.

## Examples

```json taskboard-examples
[
  {"args": ["add", "buy milk"], "stdout": {"id": 1, "title": "buy milk", "completed": false}},
  {"args": ["list"], "stdout": [{"id": 1, "title": "buy milk", "completed": false}]},
  {"args": ["complete", "1"], "stdout": {"id": 1, "title": "buy milk", "completed": true}}
]
```

## Running tests

Run all unittests with:

    python -m unittest discover tests

All tests use temporary databases and do not affect your data.
