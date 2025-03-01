import unittest
from to_do_list import ToDoList

class TestToDoList(unittest.TestCase):

    def setUp(self):
        self.todo = ToDoList()

    def test_add_task(self):
        self.todo.add_task("Buy groceries")
        self.assertIn("Buy groceries", self.todo.tasks)
        self.assertEqual(self.todo.tasks["Buy groceries"],"not done yet")

    def test_duplicate_task(self):
        self.todo.add_task("Buy groceries")
        with self.assertRaises(ValueError):
            self.todo.add_task("Buy groceries")

    def test_empty_task(self):
        with self.assertRaises(ValueError):
            self.todo.add_task("")

    def test_complete_task(self):
        self.todo.add_task("Buy groceries")
        self.todo.complete_task("Buy groceries")
        self.assertEqual(self.todo.tasks['Buy groceries'],"done")

    def test_complete_nonexistent_task(self):
        with self.assertRaises(ValueError):
            self.todo.complete_task("Buy groceries")

    def test_get_active_tasks(self):
        self.todo.add_task("Read a book")
        self.todo.add_task("Write code")
        self.todo.complete_task("Read a book")
        self.assertEqual(self.todo.get_active_tasks(), ["Write code"])

    def test_get_completed_tasks(self):
        self.todo.add_task("Meditate")
        self.todo.add_task("Exercise")
        self.todo.complete_task("Meditate")
        self.assertEqual(self.todo.get_completed_tasks(), ["Meditate"])

    def test_empty_todo_list(self):
        self.assertEqual(self.todo.get_active_tasks(), [])
        self.assertEqual(self.todo.get_completed_tasks(), [])


    if __name__ == '__main__':
        unittest.main()