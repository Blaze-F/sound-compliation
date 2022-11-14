from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import User as CustomUserModel

User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create(  # User 생성
            email=validated_data["email"],
            username=validated_data["name"],
        )
        user.set_password(validated_data["password"])

        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = "__all__"


class LoginResponseSchema(serializers.Serializer):
    access = serializers.CharField()


class UserSignUpSchema(serializers.Serializer):
    """
    user 회원가입 기능 요청 정의 입니다.
    """

    name = serializers.CharField(max_length=20, allow_null=False)
    email = serializers.CharField(max_length=100, allow_null=False)
    password = serializers.CharField(max_length=255, allow_null=False)
    district = serializers.CharField(max_length=20, allow_null=False)


class UserLoginSchema(serializers.Serializer):
    """
    user 로그인 기능 요청 정의 입니다.
    """

    email = serializers.CharField(max_length=100, allow_null=False)
    password = serializers.CharField(max_length=255, allow_null=False)
