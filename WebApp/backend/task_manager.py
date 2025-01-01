from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

# Data model for a Task
class Task(BaseModel):
    title: str
    deadline: Optional[str] = None
    completed: bool = False
    created_at: str = str(datetime.now())
    
class TaskManager:
    def __init__(self):
        self.tasks = []
        
    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_all_tasks(self) -> List[Task]:
        return self.tasks
    
    def mark_task_completed(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            return True
        return False