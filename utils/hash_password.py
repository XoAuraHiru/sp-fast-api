from passlib.context import CryptContext

class HashPassword:
    def __init__(self, password):
        self.password = password

    def create_hash(self):
        context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return context.hash(self.password)

    def verify_password(self, password):
        context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return context.verify(password, self.password)

