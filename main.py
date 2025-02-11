from fastapi import FastAPI
from core.db import engine, Base, SessionLocal
from routes.auth_routes import router as auth_router
from routes.todo_routes import router as todo_router
from utils.default_user import create_default_user

app = FastAPI(title="Todo App API")

@app.on_event("startup")
async def startup_event():
    #Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        create_default_user(db)
    finally:
        db.close()

app.include_router(auth_router)
app.include_router(todo_router, prefix="/todos", tags=["todos"])