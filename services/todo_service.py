from fastapi import HTTPException

from repositories.todo_repository import TodoRepository
from schemas.todo_schema import TodoResponse, TodoCreate, TodoUpdate


class TodoService:

    def __init__(self, repo: TodoRepository):
        self.repo = repo

    def get_all(self):
        todos = self.repo.get_all()
        return [TodoResponse.model_validate(todo) for todo in todos]

    def get_by_id(self, todo_id):
        todo = self.repo.get_by_id(todo_id)
        return TodoResponse.model_validate(todo)

    def create_todo(self, todo: TodoCreate) -> TodoResponse:
        todo = self.repo.create(todo)
        return TodoResponse.model_validate(todo)

    def update_todo(self, todo_id: int, todo: TodoUpdate) -> TodoResponse:
        todo = self.repo.update(todo_id, todo)
        return TodoResponse.model_validate(todo)

    def delete_todo(self, todo_id) -> None:
        if not self.delete_todo(todo_id):
            raise HTTPException(status_code=404, detail="todo not found")
