# app/auth/service.py
from fastapi import HTTPException, status
from utils import jwt
from schemas import user_schema as schemas
from repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, user: schemas.UserCreate) -> schemas.UserResponse:
        if self.user_repository.get_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        if self.user_repository.get_by_username(user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        hashed_password = jwt.get_password_hash(user.password)
        user_model = self.user_repository.create(user, hashed_password)
        return schemas.UserResponse.model_validate(user_model)

    def login(self, username: str, password: str) -> schemas.Token:
        user = self.user_repository.get_by_username(username)
        if not user or not jwt.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        access_token = jwt.create_access_token({"sub": str(user.id)})
        refresh_token = jwt.create_refresh_token({"sub": str(user.id)})

        return schemas.Token(
            access_token=access_token,
            refresh_token=refresh_token
        )

    def refresh_token(self, refresh_token: str) -> schemas.Token:
        payload = jwt.verify_token(refresh_token, is_refresh=True)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user_id = payload.get("sub")
        access_token = jwt.create_access_token({"sub": user_id})
        new_refresh_token = jwt.create_refresh_token({"sub": user_id})

        return schemas.Token(
            access_token=access_token,
            refresh_token=new_refresh_token
        )
