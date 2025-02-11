from fastapi import APIRouter, Depends, status
from typing import List
from schemas.todo_schema import TodoCreate, TodoResponse
from repositories.todo_repository import TodoRepository
from services.todo_service import TodoService
from core.auth import get_current_user
from core.dependencies import get_snowflake
from models.user import User

router = APIRouter()


def get_todo_service(sf_conn=Depends(get_snowflake)) -> TodoService:
    repository = TodoRepository(sf_conn)
    return TodoService(repository)


@router.post(
    "/",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new todo"
)
async def create_todo(
        todo: TodoCreate,
        current_user: User = Depends(get_current_user),
        todo_service: TodoService = Depends(get_todo_service)
) -> TodoResponse:
    return todo_service.create_todo(todo, current_user)


@router.get(
    "/",
    response_model=List[TodoResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all todos for the current user"
)
async def get_todos(
        current_user: User = Depends(get_current_user),
        todo_service: TodoService = Depends(get_todo_service)
) -> List[TodoResponse]:
    return todo_service.get_todos(current_user)


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a specific todo"
)
async def get_todo(
        todo_id: int,
        current_user: User = Depends(get_current_user),
        todo_service: TodoService = Depends(get_todo_service)
) -> TodoResponse:
    return todo_service.get_todo(todo_id, current_user)


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK
)
async def update_todo(
        todo_id: int,
        todo: TodoCreate,
        current_user: User = Depends(get_current_user),
        todo_service: TodoService = Depends(get_todo_service)
) -> TodoResponse:
    return todo_service.update_todo(todo_id, todo, current_user)


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_todo(
        todo_id: int,
        current_user: User = Depends(get_current_user),
        todo_service: TodoService = Depends(get_todo_service)
) -> None:
    todo_service.delete_todo(todo_id, current_user)
