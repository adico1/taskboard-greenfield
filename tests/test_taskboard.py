import unittest
import tempfile
import os
import json
from pathlib import Path
from taskboard import domain, storage

class TestValidation(unittest.TestCase):
    def test_blank_title(self):
        with self.assertRaises(domain.TaskboardError):
            domain.validate_title('   ')
    def test_valid_title(self):
        self.assertEqual(domain.validate_title('  foo  '), 'foo')
    def test_invalid_id(self):
        with self.assertRaises(domain.TaskboardError):
            domain.validate_id('abc')
        with self.assertRaises(domain.TaskboardError):
            domain.validate_id('-1')
        with self.assertRaises(domain.TaskboardError):
            domain.validate_id('0')

class TestStateTransitions(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix='.sqlite3')
        storage.init_db(self.db_path)
    def tearDown(self):
        os.close(self.db_fd)
        os.remove(self.db_path)
    def test_add_and_complete(self):
        task = storage.add_task(self.db_path, 'test')
        self.assertEqual(task['title'], 'test')
        self.assertFalse(task['completed'])
        completed = storage.complete_task(self.db_path, task['id'])
        self.assertTrue(completed['completed'])
        self.assertEqual(completed['id'], task['id'])
    def test_complete_idempotent(self):
        task = storage.add_task(self.db_path, 'foo')
        storage.complete_task(self.db_path, task['id'])
        again = storage.complete_task(self.db_path, task['id'])
        self.assertTrue(again['completed'])

class TestPersistence(unittest.TestCase):
    def test_persistence_across_runs(self):
        db_fd, db_path = tempfile.mkstemp(suffix='.sqlite3')
        try:
            storage.init_db(db_path)
            t1 = storage.add_task(db_path, 'persist')
            t2 = storage.add_task(db_path, 'again')
            tasks = storage.list_tasks(db_path)
            self.assertEqual(len(tasks), 2)
            self.assertEqual(tasks[0]['title'], 'persist')
            self.assertEqual(tasks[1]['title'], 'again')
        finally:
            os.close(db_fd)
            os.remove(db_path)
