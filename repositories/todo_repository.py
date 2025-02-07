from typing import List, Optional

from dns.e164 import query

from schemas.todo_schema import TodoCreate, TodoResponse
from core.dependencies import get_snowflake


class TodoRepository:
    def __init__(self):
        self.sf_conn = get_snowflake()

    @staticmethod
    def row_to_todo(row: dict) -> TodoResponse:
        return TodoResponse(
            id=row['id'],
            user_id=row['user_id'],
            title=row['title'],
            description=row['description'],
            completed=row['completed'],
            created_at=row['created_at']
        )

    def get_user_todos(self, user_id: int) -> List[TodoResponse]:
        query = """
            SELECT id, user_id, title, description, completed, created_at 
            FROM todos 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """
        todos = self.sf_conn.fetch_records(query, [user_id])
        return [self.row_to_todo(row) for row in todos]

    def create(self, todo: TodoCreate, user_id: int) -> TodoResponse:
        query = """
            INSERT INTO todos (user_id, title, description, completed)
            VALUES (%s, %s, %s, %s)
            RETURNING id, user_id, title, description, completed, created_at
        """
        params = [user_id, todo.title, todo.description, todo.completed]

        result = self.sf_conn.fetch_records(query, params)
        if not result:
            raise ValueError("Failed to create todo")

        return self.row_to_todo(result[0])

    def update(self, todo_id: int, user_id: int, todo: TodoCreate) -> Optional[TodoResponse]:

        query = """
            UPDATE todos 
            SET title = %s, description = %s, completed = %s
            WHERE id = %s AND user_id = %s
            RETURNING id, user_id, title, description, completed, created_at
        """
        params = [todo.title, todo.description, todo.completed, todo_id, user_id]

        result = self.sf_conn.fetch_records(query, params)
        return self.row_to_todo(result[0]) if result else None

    def delete(self, todo_id: int, user_id: int) -> bool:

        query = "DELETE FROM todos WHERE id = %s AND user_id = %s"
        try:
            self.sf_conn.commit_record(query, [todo_id, user_id])
            return True
        except Exception:
            return False

    def get_todo(self, todo_id: int, user_id: int) -> Optional[TodoResponse]:

        query = """
            SELECT id, user_id, title, description, completed, created_at 
            FROM todos 
            WHERE id = %s AND user_id = %s
        """
        result = self.sf_conn.fetch_records(query, [todo_id, user_id])
        return self.row_to_todo(result[0]) if result else None

    def get_all_todo(self):
        query = """
            SELECT id, user_id, title, description, completed, created_at
            FROM todos
        """

        todos = self.sf_conn.fetch_records(query, [])
        return [self.row_to_todo(row) for row in todos]