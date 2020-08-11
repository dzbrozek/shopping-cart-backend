from typing import TypedDict, cast

from django.contrib.auth import authenticate, login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer
from users.models import User


class MeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['is_admin']


class LoginSerializerData(TypedDict):
    email: str
    password: str


class LoginSerializer(Serializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField()

    def validate(self, validated_data: LoginSerializerData) -> LoginSerializerData:
        user = authenticate(email=validated_data['email'], password=validated_data['password'])

        if not user:
            raise ValidationError('Invalid credentials')

        return validated_data

    def save(self, **kwargs: dict) -> User:
        user = authenticate(email=self.validated_data['email'], password=self.validated_data['password'])

        if not user:
            raise ValidationError('Invalid credentials')

        login(self.context['request'], user)

        return cast(User, user)
