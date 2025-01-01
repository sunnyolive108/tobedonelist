import json
import os
from datetime import datetime

# Core Logic: TaskManager
class TaskManager:
    def __init__(self, data_file="tasks.json"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(script_dir, data_file)
        
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from a file."""
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_tasks(self):
        """Save tasks to a file."""
        with open(self.data_file, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, title, deadline=None):
        """Add a new task."""
        task = {
            "title": title,
            "completed": False,
            "created_at": str(datetime.now()),
            "deadline": deadline
        }
        self.tasks.append(task)
        self.save_tasks()

    def get_tasks(self):
        """Return all tasks."""
        return self.tasks

    def mark_task_completed(self, task_no):
        """Mark a task as completed."""
        if 1 <= task_no <= len(self.tasks):
            self.tasks[task_no - 1]["completed"] = True
            self.save_tasks()
            return True
        return False

# Interface Layer: CLI Implementation
class ToDoCLI:
    def __init__(self):
        self.manager = TaskManager()

    def display_tasks(self):
        """Display all tasks."""
        tasks = self.manager.get_tasks()
        if not tasks:
            print("No tasks to show!\n")
            return

        print("\nYour Tasks:")
        for i, task in enumerate(tasks, start=1):
            status = "[X]" if task["completed"] else "[ ]"
            deadline = f" (Deadline: {task['deadline']})" if task['deadline'] else ""
            print(f"{i}. {status} {task['title']}{deadline}")
        print()

    def add_task(self):
        """Prompt user to add a new task."""
        title = input("Enter task title: ")
        deadline = input("Enter deadline (YYYY-MM-DD) or leave blank: ")
        deadline = deadline if deadline else None
        self.manager.add_task(title, deadline)
        print("Task added successfully!\n")

    def mark_task_completed(self):
        """Prompt user to mark a task as completed."""
        self.display_tasks()
        try:
            task_no = int(input("Enter task number to mark as completed: "))
            if self.manager.mark_task_completed(task_no):
                print("Task marked as completed!\n")
            else:
                print("Invalid task number!\n")
        except ValueError:
            print("Please enter a valid number!\n")

    def run(self):
        """Main function for the CLI app."""
        while True:
            print("1. Add Task")
            print("2. View Tasks")
            print("3. Mark Task as Completed")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.display_tasks()
            elif choice == "3":
                self.mark_task_completed()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please try again!\n")

if __name__ == "__main__":
    app = ToDoCLI()
    app.run()
