from fastapi import FastAPI
from config.db import engine
from models.todo import Base
import controllers.todo_controller as todo
app = FastAPI(title="Todo App API")
Base.metadata.create_all(bind=engine)

app.include_router(todo.router)


