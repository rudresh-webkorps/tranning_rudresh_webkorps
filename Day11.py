from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    title: str
    done: bool = False

tasks: dict[int, Task] = {}
next_id = 1

@app.post('/tasks', status_code=201)
def create(task: Task):
    global next_id
    tasks[next_id] = task
    next_id += 1
    return {'id': next_id - 1, **task.model_dump()}

@app.get('/tasks')
def read_all():
    return tasks

@app.get('/tasks/{task_id}')
def read_one(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail='Task not found')
    return tasks[task_id]

@app.put('/tasks/{task_id}')
def update(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail='Task not found')
    tasks[task_id] = task
    return task

@app.delete('/tasks/{task_id}', status_code=204)
def delete(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail='Task not found')
    del tasks[task_id]