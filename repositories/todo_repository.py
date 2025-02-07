from typing import List, Optional
from schemas.todo_schema import TodoCreate, TodoResponse
from core.sf_connection import SnowflakeConnector


class TodoRepository:
    SELECT_TODO_FIELDS = """
        SELECT id, user_id, title, description, priority, completed, created_at
        FROM todos
    """

    INSERT_TODO = """
        INSERT INTO todos (title, description, priority, completed, user_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    UPDATE_TODO = """
        UPDATE todos 
        SET title = %s, description = %s, priority = %s, completed = %s
        WHERE id = %s AND user_id = %s
    """

    DELETE_TODO = "DELETE FROM todos WHERE id = %s AND user_id = %s"

    SELECT_LAST_INSERTED = """
        SELECT id, user_id, title, description, priority, completed, created_at
        FROM todos 
        WHERE user_id = %s 
        ORDER BY created_at DESC 
        LIMIT 1
    """

    def __init__(self, sf_conn: SnowflakeConnector):
        self.sf_conn = sf_conn

    @staticmethod
    def row_to_todo(row: dict) -> TodoResponse:
        return TodoResponse(
            id=row['ID'],
            user_id=row['USER_ID'],
            title=row['TITLE'],
            description=row['DESCRIPTION'],
            priority=row['PRIORITY'],
            completed=row['COMPLETED'],
            created_at=row['CREATED_AT']
        )

    def create(self, todo: TodoCreate, user_id: int) -> Optional[TodoResponse]:
        self.sf_conn.commit_record(
            self.INSERT_TODO,
            [todo.title, todo.description, todo.priority, todo.completed, user_id]
        )

        result = self.sf_conn.fetch_records(self.SELECT_LAST_INSERTED, [user_id])
        return self.row_to_todo(result[0]) if result else None

    def get_todos(self, user_id: int) -> List[TodoResponse]:
        query = f"{self.SELECT_TODO_FIELDS} WHERE user_id = %s"
        result = self.sf_conn.fetch_records(query, [user_id])
        return [self.row_to_todo(row) for row in result]

    def get_todo(self, todo_id: int, user_id: int) -> Optional[TodoResponse]:
        query = f"{self.SELECT_TODO_FIELDS} WHERE id = %s AND user_id = %s"
        result = self.sf_conn.fetch_records(query, [todo_id, user_id])
        return self.row_to_todo(result[0]) if result else None

    def update(self, todo_id: int, user_id: int, todo: TodoCreate) -> Optional[TodoResponse]:
        self.sf_conn.commit_record(
            self.UPDATE_TODO,
            [todo.title, todo.description, todo.priority, todo.completed, todo_id, user_id]
        )
        return self.get_todo(todo_id, user_id)

    def delete(self, todo_id: int, user_id: int) -> bool:
        try:
            self.sf_conn.commit_record(self.DELETE_TODO, [todo_id, user_id])
            return True
        except Exception:
            return False