from user.models import User
from user.serializers import UserSerializer
from exceptions import NotFoundError


class AbstractUserRepo:
    def __init__(self) -> None:
        self.model = User
        self.serializer = UserSerializer


class UserRepo(AbstractUserRepo):
    def get(self, user_id: int) -> dict:
        try:
            return UserSerializer(self.model.objects.get(id=user_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def get_by_email(self, email: str):
        try:
            return UserSerializer(self.model.objects.get(email=email)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def create(self, name: str, email: str, password: str):
        serializer = self.serializer(
            data={
                "name": name,
                "email": email,
                "password": password,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
