import argparse
import json
import sys
from pathlib import Path
from . import domain, storage

def main():
    parser = argparse.ArgumentParser(prog="taskboard")
    parser.add_argument('--database', default='tasks.sqlite3', help='Path to SQLite database')
    subparsers = parser.add_subparsers(dest='command', required=True)

    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Title of the task')

    list_parser = subparsers.add_parser('list', help='List all tasks')

    complete_parser = subparsers.add_parser('complete', help='Mark a task as completed')
    complete_parser.add_argument('id', help='ID of the task to complete')

    args = parser.parse_args()
    db_path = Path(args.database)
    try:
        storage.init_db(db_path)
        if args.command == 'add':
            title = domain.validate_title(args.title)
            task = storage.add_task(db_path, title)
            print(json.dumps(task), flush=True)
            sys.exit(0)
        elif args.command == 'list':
            tasks = storage.list_tasks(db_path)
            print(json.dumps(tasks), flush=True)
            sys.exit(0)
        elif args.command == 'complete':
            task_id = domain.validate_id(args.id)
            task = storage.complete_task(db_path, task_id)
            print(json.dumps(task), flush=True)
            sys.exit(0)
    except domain.TaskboardError as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr, flush=True)
        sys.exit(2)
    except Exception as e:
        print(json.dumps({'error': 'Internal error'}), file=sys.stderr, flush=True)
        sys.exit(2)
