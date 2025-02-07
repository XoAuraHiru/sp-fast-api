from fastapi import HTTPException
from typing import List
from models.user import User
from repositories.todo_repository import TodoRepository
from schemas.todo_schema import TodoCreate, TodoResponse, TodoUpdate

class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def create_todo(self, todo: TodoCreate, user: User) -> TodoResponse:
        try:
            created_todo = self.repository.create(todo, user.id)
            if not created_todo:
                raise HTTPException(status_code=400, detail="Could not create todo")
            return created_todo
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_todos(self, user: User) -> List[TodoResponse]:
        try:
            return self.repository.get_todos(user.id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_todo(self, todo_id: int, user: User) -> TodoResponse:
        todo = self.repository.get_todo(todo_id, user.id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

    def update_todo(self, todo_id: int, todo: TodoUpdate, user: User) -> TodoResponse:
        updated_todo = self.repository.update(todo_id, user.id, todo)
        if not updated_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return updated_todo

    def delete_todo(self, todo_id: int, user: User) -> bool:
        if not self.repository.delete(todo_id, user.id):
            raise HTTPException(status_code=404, detail="Todo not found")
        return True