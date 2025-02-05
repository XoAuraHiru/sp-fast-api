from fastapi import FastAPI
from core.config.db import engine, Base
from routes.todo_routes import router as todo_router
from models.todo import Todo
from models.user import User
app = FastAPI(title="Todo App API")
Base.metadata.create_all(bind=engine)

app.include_router(todo_router, prefix="/todos", tags=["todos"])