from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from core.config.db import get_db
from repositories.todo_repository import TodoRepository
from schemas.todo_schema import TodoResponse, TodoCreate, TodoUpdate
from services.todo_service import TodoService

router = APIRouter()

def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    todo_repository = TodoRepository(db)
    return TodoService(todo_repository)

@router.get("/", response_model=List[TodoResponse])
def get_todos(
    todo_service: TodoService = Depends(get_todo_service)
):
    return todo_service.get_all()

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    todo_service: TodoService = Depends(get_todo_service)
):
    return todo_service.create_todo(todo)

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    todo_service: TodoService = Depends(get_todo_service)
):
    return todo_service.get_by_id(todo_id)

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    todo_service: TodoService = Depends(get_todo_service)
):
    return todo_service.update_todo(todo_id, todo)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    todo_service: TodoService = Depends(get_todo_service)
):
    todo_service.delete_todo(todo_id)
