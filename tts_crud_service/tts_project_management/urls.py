from django.urls import path

from tts_project_management.views import (
    ProjectView,
    audio_data_update,
    delete_audio_data,
    insert_data,
)


urlpatterns = [
    path("project/", ProjectView.as_view()),
    path("project/push/", insert_data),
    path("project/audio/update/", audio_data_update),
    path("project/audio/delete", delete_audio_data),
]
