from django.core.mail import send_mail
from .permission import (IsAdmin,
                         IsAuthenticatedOrReadOnly,
                         IsModeratorIsOwnerOrReadOnly)
from .serializers import (UserSerializer,
                          UserEditSerializer,
                          RegistraterUserSerializer,
                          TokenUserSerializer)
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from reviews.models import User
from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from rest_framework.simplejwt.tokens import AssertToken
from rest_framework import viewsets


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serialized = RegistraterUserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        user = get_object_or_404(
            User, useername=serializers.validated_data['username']
        )
        confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация',
        message=f'Ваш токен {confirmation_code}',
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False
    )
    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer=TokenUserSerializer(data=request.data)
    serializer.is_valid()
    user = get_object_or_404(
            User, useername=serializers.validated_data['username']
        )
    if default_token_generator.check_token(
        user.serializer.validated_data['confirmation_code']
    ):
        token = AssertToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path = 'me',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def users_profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
