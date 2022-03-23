from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User

from .permissions import RetrievePermission
from .serializers import SetPasswordSerializer, UserSerializer
from .utils import PageLimitPaginator


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageLimitPaginator
    permission_classes = (RetrievePermission,)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['POST'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def set_password(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']
        username = request.user.username
        user = get_object_or_404(
            User,
            username=username
        )
        if check_password(password, user.password):
            user.set_password(new_password)
            user.save()
            return Response(
                'Пароль измененен', status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            'Неверный пароль', status=status.HTTP_400_BAD_REQUEST
        )


# @api_view(['POST'])
# def get_token(request):
#     serializer = AuthTokenSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     email = serializer.validated_data['email']
#     password = serializer.validated_data['password']
#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return Response(
#             'Пользователь не найден', status=status.HTTP_404_NOT_FOUND
#         )
#     if check_password(password, user.password):
#         refresh = RefreshToken.for_user(user)
#         token_data = {'token': str(refresh.access_token)}
#         return Response(token_data, status=status.HTTP_200_OK)
#     return Response('Неверный пароль', status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def delete_token(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         user = User.objects.get(username=username)
#         old_token = TokenObtainPairSerializer.get_token(user)
#         old_token.blacklist()
#         return Response(
#             'Токен удален',
#             status=status.HTTP_204_NO_CONTENT
#         )
#     return Response(
#         'Пользователь не авторизован',
#         status=status.HTTP_401_UNAUTHORIZED
#     )
    # header = request.headers['Authorization']
    # header2 = header[7:]
    # # token = RefreshToken(header2)
    # # token.blacklist()
    # return Response(
    #     header2,
    #     status=status.HTTP_204_NO_CONTENT
    # )
    #     refresh = RefreshToken.for_user(user)
    #     refresh.blacklist()
