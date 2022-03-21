from rest_framework.decorators import api_view, action
from rest_framework import viewsets, status
from users.models import User
from .serializers import (
    UserSerializer,
    AuthTokenSerializer,
    SetPasswordSerializer
)
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=True,
        methods=['GET']
    )
    def me(self, request):
        if request.user.is_authenticated():
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['PUT']
    )
    def set_password(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['current_password']
        username = request.user.username
        user = User.objects.get_object_or_404(
            User,
            username=username
        )
        if user.password == password:
            user.password = serializer.validated_data['new_password']
        return Response(
            'Неверный пароль', status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def get_token(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            'Пользователь не найден', status=status.HTTP_404_NOT_FOUND
        )
    if user.password == password:
        refresh = RefreshToken.for_user(user)
        token_data = {'token': str(refresh.access_token)}
        return Response(token_data, status=status.HTTP_200_OK)
    return Response(
        'Неверный пароль', status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
def delete_token(request):
    if request.user.is_authenticated():
        username = request.user.username
        user = get_object_or_404(User, username=username)
        RefreshToken.for_user(user)
