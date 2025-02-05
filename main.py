from fastapi import FastAPI
from core.config.db import engine, Base
from routes.todo_routes import router as todo_router
app = FastAPI(title="Todo App API")
Base.metadata.create_all(bind=engine)

app.include_router(todo_router, prefix="/todos", tags=["todos"])