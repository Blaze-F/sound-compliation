from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from decorator.execption_handler import execption_hanlder
from user.provider.auth_provider import AuthProvider
from user.serializers import (
    LoginResponseSchema,
    UserLoginSchema,
    UserSignUpSchema,
    UserSignupSerializer,
)
from user.service import UserService

user_service = UserService()
auth_provider = AuthProvider()


@swagger_auto_schema(
    method="post",
    request_body=UserLoginSchema,
    operation_description="JWT 토큰이 반환됩니다. 헤더에 넣어주세요",
    responses={200: LoginResponseSchema},
)
@api_view(["POST"])
@execption_hanlder()
@parser_classes([JSONParser])
def login(request):
    email = request.data["email"]
    password = request.data["password"]
    auth_token = auth_provider.login(email, password)
    return JsonResponse(auth_token, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="post",
    request_body=UserSignUpSchema,
    responses={201: UserSignupSerializer},
)
@api_view(["POST"])
@execption_hanlder()
@parser_classes([JSONParser])
def signup(request):
    params = request.data
    params = UserSignUpSchema(data=params)
    params.is_valid(raise_exception=True)
    created_user = user_service.create(**params.data)
    return JsonResponse(created_user, status=status.HTTP_201_CREATED)


# @api_view(["POST"])
# @execption_hanlder()
# @parser_classes([JSONParser])
# @swagger_auto_schema(
#     responses={"access": "encoded_jwt"},
# )
# def signout(request):
#     auth_token = request.META.get("HTTP_AUTHORIZATION", None)
#     if auth_token != None:
#         auth_token = auth_provider.logout(auth_token)
#     return JsonResponse(auth_token, status=status.HTTP_200_OK)
