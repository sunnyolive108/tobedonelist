from fastapi import APIRouter
from task_manager import Task, TaskManager

router = APIRouter()

task_manager = TaskManager()

@router.post("/tasks/")
def add_task(task: Task):
    task_manager.add_task(task)
    return {"message": "Task added successfully"}

@router.get("/tasks/", response_model=list[Task])
def get_tasks():
    return task_manager.get_all_tasks()

@router.put("/tasks/{task_id}/complete/")
def mark_task_completed(task_id: int):
    success = task_manager.mark_task_completed(task_id)
    if success:
        return {"message": "Task completed"}
    else:
        return {"message": "ID not found"}