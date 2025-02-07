from fastapi import HTTPException, status
from typing import List, Optional
from repositories.todo_repository import TodoRepository
from schemas.todo_schema import TodoCreate, TodoResponse


class TodoService:
    def __init__(self, todo_repository: TodoRepository):
        self.repository = todo_repository

    def get_user_todos(self, user_id: int) -> List[TodoResponse]:
        return self.repository.get_user_todos(user_id)

    def create_todo(self, todo: TodoCreate, user_id: int) -> TodoResponse:
        try:
            return self.repository.create(todo, user_id)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    def update_todo(self, todo_id: int, todo: TodoCreate, user_id: int) -> TodoResponse:
        updated_todo = self.repository.update(todo_id, user_id, todo)
        if not updated_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or unauthorized"
            )
        return updated_todo

    def delete_todo(self, todo_id: int, user_id: int) -> None:
        if not self.repository.delete(todo_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or unauthorized"
            )

    def get_todo(self, todo_id: int, user_id: int) -> TodoResponse:
        todo = self.repository.get_todo(todo_id, user_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or unauthorized"
            )
        return todo

    def get_all_todos(self):
        todo = self.repository.get_all_todo()
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        return todo