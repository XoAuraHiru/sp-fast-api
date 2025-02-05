from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.config.db import get_db
from repositories.user_repository import UserRepository
from schemas.user_schema import UserResponse
from services.user_service import UserService

router = APIRouter()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    user_repository = UserRepository(db)
    return UserService(user_repository)

@router.get("/", response_model=list[UserResponse])
def get_users(
    user_service: UserService = Depends(get_user_service)
):
    return user_service.get_all()