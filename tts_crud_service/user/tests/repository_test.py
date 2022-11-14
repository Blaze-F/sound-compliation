import pytest
from django.conf import settings
from user.repository import UserRepo

user_repo = UserRepo()


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


@pytest.mark.django_db()
def test_create_user():
    sut = user_repo.create(
        **{
            "name": "test",
            "email": "test@test.com",
            "district": "강남구",
            "password": "test_pwd",
        }
    )
    isinstance(sut, dict)
