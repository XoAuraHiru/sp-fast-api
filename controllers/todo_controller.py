# from typing import Annotated
#
# from fastapi import APIRouter, Depends, Path, HTTPException
# from pydantic import BaseModel, Field
# from sqlalchemy.orm import Session
# from starlette import status
# from config.db import get_db
# from models.todo import Todos
#
# router = APIRouter(
#     prefix="/todos",
#     tags=["todos"]
# )
#
# DB = Annotated[Session, Depends(get_db)]
#
# class TodoRequest(BaseModel):
#     title: str = Field(min_length=3, max_length=100)
#     description: str = Field(min_length=3, max_length=1000)
#     priority: int = Field(gt=0, lt=6)
#     completed: bool = False
#
#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "title": "Buy groceries",
#                 "description": "Buy milk, eggs, and bread",
#                 "priority": 3,
#                 "completed": False
#             }
#         }
#
#
# @router.get("/", status_code=status.HTTP_200_OK, response_model=list[TodoRequest])
# async def read_all(db: Session = Depends(get_db)):
#     return db.query(Todos).all()
#
#
# @router.get("/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoRequest)
# async def read_todo(todo_id: int = Path(gt=0), db: Session = Depends(get_db)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is not None:
#         return todo_model
#     raise HTTPException(status_code=404, detail="todo not found")
#
#
# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=TodoRequest)
# async def create_todo(todo_request: TodoRequest, db: Session = Depends(get_db)):
#     todo_model = Todos(**todo_request.model_dump())
#     db.add(todo_model)
#     db.commit()
#     return todo_model
#
#
# @router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
# async def update_todo(todo_request: TodoRequest, todo_id: int = Path(gt=0), db: Session = Depends(get_db)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail="todo not found")
#
#     todo_model.title = todo_request.title
#     todo_model.description = todo_request.description
#     todo_model.priority = todo_request.priority
#     todo_model.completed = todo_request.completed
#
#     db.add(todo_model)
#     db.commit()
#
#
# @router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
# async def delete_todo(todo_id: int = Path(gt=0), db: Session = Depends(get_db)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail='Todo not found.')
#     db.query(Todos).filter(Todos.id == todo_id).delete()
#     db.commit()