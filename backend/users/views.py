from django.contrib import messages
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from api.pagination import CustomPagination
from users.models import Subscription, User

from .serializers import (CreateUserSerializer, PasswordChangeSerializer,
                          SubscriptionCreateSerializer, SubscriptionSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """Basic User Viewset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ('list', 'create'):
            self.permission_classes = (AllowAny,)
        return super(UserViewSet, self).get_permissions()

    def me(self, request, *args, **kwargs):
        user = self.request.user
        user_data = UserSerializer(user)
        return Response(user_data.data)


class ChangePasswordView(viewsets.ModelViewSet):
    serializer_class = PasswordChangeSerializer
    model = User

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not self.object.check_password(
            serializer.validated_data.get("current_password")
        ):
            return Response(
                {"current_password": ["Wrong password"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        if serializer.is_valid():
            self.object.set_password(serializer.validated_data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password changed successfully',
                'data': []
            }
            return Response(response)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """Subscription viewset"""
    pagination_class = CustomPagination

    def get_queryset(self):
        return User.objects.filter(subs__user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return SubscriptionSerializer
        return SubscriptionCreateSerializer

    def perform_destroy(self, instance, pk):
        author = get_object_or_404(
            User,
            pk=pk
        )
        obj = get_object_or_404(
            Subscription,
            author=author,
            user=self.request.user
        )
        obj.delete()
        return Response(status=HTTP_204_NO_CONTENT)
