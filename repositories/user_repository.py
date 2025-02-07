from sqlalchemy.orm import Session
from models import user as model
from schemas import user_schema as schemas
from typing import Optional


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[model]:
        return self.db.query(model).filter(model.username == username).first()

    def get_by_email(self, email: str) -> Optional[model]:
        return self.db.query(model).filter(model.email == email).first()

    def create(self, user: schemas.UserCreate, hashed_password: str) -> model:
        db_user = model(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user