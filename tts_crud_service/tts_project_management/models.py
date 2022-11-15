from django.db import models

from tts_crud_service.models import BaseModel
from user.models import User


class TtsProject(BaseModel):
    project_title = models.CharField(null=False, unique=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")


class AudioData(BaseModel):
    text = models.CharField(null=False, max_length=255)
    slow = models.FloatField(null=False, default=False)
    tts_project = models.ForeignKey(TtsProject, on_delete=models.CASCADE, db_column="project_id")
    name = models.CharField(max_length=255, null=False)
