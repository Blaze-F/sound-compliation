from django.db import models

from tts_crud_service.models import BaseModel


class TtsProjects(BaseModel):
    project_title = models.CharField(null=False)


class AudioData(BaseModel):
    text = models.CharField(null=False)
    speed = models.FloatField(null=False, default=1)
    tts_project = models.ForeignKey(TtsProjects, on_delete=models.CASCADE, db_column="project_id")
    is_file_exisist = models.BooleanField(null=False,default=False)
    saved_path = models.CharField(max_length=255, null=True)