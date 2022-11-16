import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from decorator.auth_handler import must_be_user
from decorator.execption_handler import execption_hanlder
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, IN_QUERY

from tts_project_management.repository import (
    AudioDataRepository,
    TtsProjectRepository,
)
from rest_framework.views import APIView
from tts_project_management.serializer import (
    AudioDataInsertReqSchema,
    AudioDataSerializer,
    TtsProjectCreateSchema,
)
from tts_project_management.service import AudioDataManagementService, TtsProjectManagementService
from tts_project_management.utils.preprocess import preprocess_data

# 인스턴스 생성
tts_project_repository = TtsProjectRepository()
audio_data_repository = AudioDataRepository()
service = TtsProjectManagementService(
    tts_project_repo=tts_project_repository, audio_data_repo=audio_data_repository
)
audio_service = AudioDataManagementService(
    tts_project_repo=tts_project_repository, audio_data_repo=audio_data_repository
)


class ProjectView(APIView):
    def post(self, request, *args, **kwargs):
        return project_create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return find_project_page(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return project_delete(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return project_update(request, *args, **kwargs)


@swagger_auto_schema(responses={200: dict}, request_body=json)
# @execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def project_create(request):
    user_id = request.user["id"]
    data = request.data
    input = TtsProjectCreateSchema(data=data)
    input.is_valid(raise_exception=True)
    project_title = data["project_title"]
    # 전처리기 호출
    sentenses = preprocess_data(input=data["sentenses"])

    created = service.create_project(
        user_id=user_id, project_title=project_title, project_container=sentenses
    )

    return JsonResponse(created, status=201, safe=False)


@swagger_auto_schema(responses={200: AudioDataSerializer})
@execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def find_project_page(request):
    user_id = request.user["id"]
    project_title = request.GET["project_title"]
    pagenum = request.get["page"]
    data_list = service.get_page(projct_title=project_title, page=pagenum)

    return JsonResponse(data_list, status=200)


@swagger_auto_schema(
    responses={200: dict},
)
@execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def project_delete(request):
    user_id = request.user["id"]
    project_title = request.GET["project_title"]
    res = service.delete_project(project_title=project_title)
    return JsonResponse(res, status=200)


@swagger_auto_schema(
    method="post", responses={200: AudioDataSerializer}, request_body=AudioDataInsertReqSchema
)
@api_view(["POST"])
# @execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def insert_data(request):
    user_id = request.user["id"]
    data = request.data
    input = AudioDataInsertReqSchema(data=data)
    input.is_valid(raise_exception=True)
    # 전처리기 호출
    sentenses = preprocess_data(input=data["sentenses"])
    project_title = data["project_title"]
    sequence = data["sequence"]

    res = audio_service.insert_audio_data(
        data=sentenses, sequence=sequence, project_title=project_title
    )
    return JsonResponse(res, status=200)


@swagger_auto_schema(
    method="put", request_body=AudioDataInsertReqSchema, responses={200: AudioDataSerializer}
)
@api_view(["PUT"])
@execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def audio_data_update(request):
    user_id = request.user["id"]
    data = request.data
    sentense = data["sentense"]
    sequence = data["sequence"]
    project_title = data["project_title"]

    updated = audio_service.update_audio_data(
        sentense=sentense, sequence=sequence, project_title=project_title
    )

    return JsonResponse(updated, status=200)


@swagger_auto_schema(
    method="delete", responses={200: AudioDataSerializer}, request_body=AudioDataInsertReqSchema
)
@api_view(["DELETE"])
@execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def delete_audio_data(request):
    user_id = request.user["id"]
    data = request.data
    project_title = data["project_title"]
    sequence = data["sequence"]

    res = audio_service.delete_audio_data(
        project_title=project_title, sequence=sequence, slow=False
    )
    return JsonResponse(res, status=200)
