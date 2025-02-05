from repositories.user_repository import UserRepository
from schemas.user_schema import UserResponse


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_all(self):
        users = self.repo.get_all()
        return [UserResponse.model_validation(user) for user in users]
