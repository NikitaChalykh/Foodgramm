from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow, User
from .permissions import RetrievePermission
from .serializers import (FollowSerializer, SetPasswordSerializer,
                          UserSerializer)
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
        serializer = UserSerializer(request.user, context={'request': request})
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
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = request.user.follower.all()
        serializer = FollowSerializer(
            queryset,
            context={'request': request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscribeViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, user_id):
        follow_author = get_object_or_404(User, pk=user_id)
        if follow_author != request.user and (
            not request.user.follower.filter(author=follow_author).exists()
        ):
            Follow.objects.create(
                user=request.user,
                author=follow_author
            )
            serializer = UserSerializer(
                follow_author, context={'request': request}
            )
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, user_id):
        follow_author = get_object_or_404(User, pk=user_id)
        data_follow = request.user.follower.filter(author=follow_author)
        if data_follow.exists():
            data_follow.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        return Response(status.HTTP_400_BAD_REQUEST)
