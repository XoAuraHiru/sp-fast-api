from sqlalchemy.orm import Session
from models.user import User
from core.security import get_password_hash

DEFAULT_USER = {
    "email": "admin@example.com",
    "username": "admin",
    "password": "admin123"
}


def create_default_user(db: Session) -> None:
    user = db.query(User).filter(User.email == DEFAULT_USER["email"]).first()
    if not user:
        user = User(
            email=DEFAULT_USER["email"],
            username=DEFAULT_USER["username"],
            hashed_password=get_password_hash(DEFAULT_USER["password"]),
            is_active=True
        )
        db.add(user)
        db.commit()
