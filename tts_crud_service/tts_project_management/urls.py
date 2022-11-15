from django.urls import path

from tts_project_management.views import ProjectView


urlpatterns = [path("project/", ProjectView.as_view())]
