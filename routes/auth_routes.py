from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.db import get_db
from services.auth_service import AuthService
from repositories.auth_repository import AuthRepository
from schemas.user_schema import UserCreate, Token

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repository = AuthRepository(db)
    return AuthService(repository)

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
) -> Token:
    return auth_service.register(user)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
) -> Token:
    return auth_service.login(form_data.username, form_data.password)