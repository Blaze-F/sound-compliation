from user.provider.auth_provider import auth_provider
from user.repository import UserRepo


class UserService:
    def __init__(self) -> None:
        self.repo = UserRepo()

    def create(self, email: str, password: str, name: str, district: str) -> dict:
        password = auth_provider.hashpw(password)
        created_user = self.repo.create(
            name=name,
            email=email,
            password=password,
            district=district,
        )
        return created_user
