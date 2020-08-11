from django.contrib.auth import logout
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from users.models import User
from users.serializers import LoginSerializer, MeSerializer


class MeAPIView(RetrieveAPIView):
    serializer_class = MeSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(MeSerializer(user).data, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        logout(request)

        return Response(status=status.HTTP_204_NO_CONTENT)
