from fastapi import FastAPI
import models
from config.db import engine

app = FastAPI(title="Todo App API")
models.Base.metadata.create_all(bind=engine)
@app.get("/")
async def root():
    return {"message": "Hello World"}