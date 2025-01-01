from fastapi import FastAPI
from api import router as task_router

app = FastAPI()

# Include task manager routes
app.include_router(task_router)