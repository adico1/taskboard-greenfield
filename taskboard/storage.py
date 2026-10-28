import sqlite3
from contextlib import closing

def init_db(db_path):
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()

def add_task(db_path, title):
    with closing(sqlite3.connect(db_path)) as conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, completed) VALUES (?, 0)", (title,)
        )
        task_id = cur.lastrowid
        conn.commit()
        cur = conn.execute(
            "SELECT id, title, completed FROM tasks WHERE id = ?", (task_id,)
        )
        row = cur.fetchone()
        return _row_to_task(row)

def list_tasks(db_path):
    with closing(sqlite3.connect(db_path)) as conn:
        cur = conn.execute(
            "SELECT id, title, completed FROM tasks ORDER BY id ASC"
        )
        return [_row_to_task(row) for row in cur.fetchall()]

def complete_task(db_path, task_id):
    with closing(sqlite3.connect(db_path)) as conn:
        cur = conn.execute(
            "SELECT id, title, completed FROM tasks WHERE id = ?", (task_id,)
        )
        row = cur.fetchone()
        if not row:
            raise Exception("Task not found.")
        conn.execute(
            "UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,)
        )
        conn.commit()
        return _row_to_task((row[0], row[1], 1))

def _row_to_task(row):
    return {
        "id": row[0],
        "title": row[1],
        "completed": bool(row[2])
    }
