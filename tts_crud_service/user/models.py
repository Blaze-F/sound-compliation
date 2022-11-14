from django.db import models

from rainy_day.models import BaseModel


class User(BaseModel):
    name = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=100, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    district = models.CharField(max_length=5, null=False)  # 회원가입시 입력하는 지역명

    class Meta:
        db_table = "user"
