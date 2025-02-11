from fastapi import HTTPException, status
from schemas.user_schema import UserCreate, Token
from repositories.auth_repository import AuthRepository
from core.security import get_password_hash, verify_password, create_access_token, create_refresh_token


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def register(self, user: UserCreate) -> Token:
        if self.repository.get_user_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        if self.repository.get_user_by_username(user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        hashed_password = get_password_hash(user.password)
        user = self.repository.create_user(user, hashed_password)

        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        return Token(access_token=access_token, refresh_token=refresh_token)

    def login(self, username: str, password: str) -> Token:
        user = self.repository.get_user_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        return Token(access_token=access_token, refresh_token=refresh_token)

    def refresh_tokens(self, payload: dict) -> Token:
        user_id = payload.get("sub")
        user = self.repository.get_user_by_id(int(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        return Token(access_token=access_token, refresh_token=refresh_token)