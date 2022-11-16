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
from tts_project_management.serializer import AudioDataSerializer, TtsProjectCreateSchema
from tts_project_management.service import TtsProjectManagementService
from tts_project_management.utils.preprocess import preprocess_data

# 인스턴스 생성
tts_project_repository = TtsProjectRepository()
audio_data_repository = AudioDataRepository()
service = TtsProjectManagementService(
    tts_project_repo=tts_project_repository, audio_data_repo=audio_data_repository
)


class ProjectView(APIView):
    def post(self, request, *args, **kwargs):
        return project_create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return find_project_page(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return project_delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return project_update(request, *args, **kwargs)


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
def project_update(request):
    user_id = request.user["id"]
    updated = service.update_project()

    return JsonResponse(updated, status=200)


@swagger_auto_schema(responses={200: AudioDataSerializer})
@execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def find_project_page(request):
    user_id = request.user["id"]
    project_title = request.GET["title"]
    pagenum = request.get["page"]
    data_list = service.get_page(projct_title=project_title, page=pagenum)

    return JsonResponse(data_list, status=200)


@swagger_auto_schema(
    manual_parameters=[Parameter("account_id", IN_QUERY, "생성 아이디 입니다.", type="int")],
    responses={200: dict},
)
@execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def project_delete(request):
    user_id = request.user["id"]
    project_title = request.GET["title"]
    res = service.delete_project(project_title=project_title)
    return JsonResponse(res, status=200)


@swagger_auto_schema(
    method="post",
    manual_parameters=[
        Parameter("account_id", IN_QUERY, "생성 아이디 입니다. 쿼리스트링입니다.", type="int"),
    ],
    responses={200: AccountSerializer},
)
@api_view(["POST"])
@execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def account_get(request):
    user_id = request.user["id"]
    account_id = request.GET["account_id"]
    res = account_book_service.get(account_id=account_id, user_id=user_id)
    return JsonResponse(res, status=200)


# @swagger_auto_schema(method="get",manual_parameters=[
#             Parameter('account_id', IN_QUERY,
#                       '생성 아이디 입니다.',
#                       type='int'),
#         ], responses={200: AccountSerializer})
# @api_view(["GET"])
# @execption_hanlder()
# @must_be_user()
# @parser_classes([JSONParser])
# def account_find_all(request):
#     user_id = request.user["id"]
#     res = account_book_service.find(user_id=user_id)

#     return JsonResponse(res, safe=False, status=200)

# @swagger_auto_schema(method="get",manual_parameters=[
#             Parameter('account_id', IN_QUERY,
#                       '생성 아이디 입니다. 쿼리스트링입니다.',
#                       type='int'),
#         ], responses={200: AccountSerializer})
# @api_view(["GET"])
# @execption_hanlder()
# @must_be_user()
# @parser_classes([JSONParser])
# def account_recover(request):
#     user_id = request.user["id"]
#     account_id = request.GET["account_id"]
#     res = account_book_service.recover(user_id=user_id, account_id=account_id)
#     return JsonResponse(res, status=200)
