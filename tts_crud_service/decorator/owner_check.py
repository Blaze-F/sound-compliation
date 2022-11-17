from functools import wraps
from tts_project_management.service import TtsProjectManagementService
from user.provider.auth_provider import auth_provider
from exceptions import NotAuthorizedError
from rest_framework.views import APIView


def owner_check():
    def decorator(api_func):
        @wraps(api_func)
        def _wrapped_view(request, *args, **kwargs):
            request = request.request if isinstance(request, APIView) else request
            auth_token = auth_provider.get_token_from_request(request)
            if auth_token == None:
                raise NotAuthorizedError
            user = auth_provider.check_auth(auth_token)
            request.user = user
            project = TtsProjectManagementService.get_project_info_by_title(
                request.data["project_title"]
            )

            if request.user[id] != project["user_id"]:
                raise NotAuthorizedError
            return api_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
