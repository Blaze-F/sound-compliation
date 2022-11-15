from django.db import models

from tts_crud_service.models import BaseModel
from user.models import User


class TtsProject(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    project_title = models.CharField(null=False, unique=True, max_length=100)

    class Meta:
        db_table = "project"


class AudioData(BaseModel):
    tts_project = models.ForeignKey(TtsProject, on_delete=models.CASCADE, db_column="project_id")
    text = models.CharField(null=False, max_length=255)
    slow = models.FloatField(null=False, default=False)
    name = models.CharField(max_length=255)
    sequense = models.IntegerField(null=True)
    path = models.CharField(max_length=255)

    class Meta:
        db_table = "audio_data"
