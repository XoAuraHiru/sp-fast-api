from typing import Type

from sqlalchemy.orm import Session

from models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Type[User]]:
        return self.db.query(User).all()
