
class ToDoList:

    def __init__(self):
        self.tasks = {}

    def add_task(self, task):

        if task.strip() == "":
            raise ValueError("Task should not be empty")

        if task not in self.tasks:
            self.tasks[task] = "not done yet"
        else:
            raise ValueError("Task already exists")

    def complete_task(self, task):

        if task in self.tasks:
            self.tasks[task] = "done"
        else:
            raise ValueError("Task does not exist")

    def get_active_tasks(self):

        return [task for task,status in self.tasks.items() if status == "not done yet"]

    def get_completed_tasks(self):

        return [task for task,status in self.tasks.items() if status == "done"]






