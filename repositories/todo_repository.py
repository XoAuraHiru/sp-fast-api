from typing import List, Type, Optional

from sqlalchemy.orm import Session

from models.todo import Todo
from schemas.todo_schema import TodoCreate, TodoUpdate


class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Type[Todo]]:
        return self.db.query(Todo).all()

    def get_by_id(self, todo_id: int) -> Optional[list[Type[Todo]]]:
        return self.db.query(Todo).filter(Todo.id == todo_id).first()

    def create(self, todo: TodoCreate):
        db_todo = Todo(**todo.model_dump())
        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo

    def update(self, todo_id: int, todo: TodoUpdate)-> Optional[Todo]:
        db_todo=self.get_by_id(todo_id)
        if db_todo:
            todo_data = todo.model_dump(exclude_unset=True)
            for key, value in todo_data.items():
                setattr(db_todo, key, value)
            self.db.commit()
            self.db.refresh(db_todo)
        return db_todo

    def delete(self, todo_id: int) -> bool:
        db_todo=self.get_by_id(todo_id)
        if db_todo:
            self.db.delete(db_todo)
            self.db.commit()
            self.db.refresh(db_todo)
            return True
        return False