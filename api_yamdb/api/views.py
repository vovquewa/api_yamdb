from django.core.mail import send_mail
from .permission import (IsAdmin,
                         IsAuthenticatedOrReadOnly,
                         IsModeratorIsOwnerOrReadOnly)
from .serializers import (UserSerializer,
                          UserEditSerializer,
                          RegistraterUserSerializer,
                          TokenUserSerializer,
                          CommentSerializer,
                          RewiewSerializer)
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from reviews.models import User
from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend


from reviews.models import Categories, Genre, Title, Review, Comment

from .serializers import CategoriesSerializer, GenreSerializer, TittleSerializer



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
        token = AccessToken.for_user(user)
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


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_field = ('name', )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_field = ('name',)


class TittleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TittleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('category', 'genre', 'name', 'year')


class ReviewViewset(viewsets.ModelViewSet):
    serializer_class = RewiewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review_queryset = title.reviews.all()
        return review_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        author = self.request.user
        if Review.objects.filter(title=title, author=author).exists():
            raise ValidationError('Возможен только один отзыв для автора')
        serializer.save(author=author, title=title)


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs['title_id']
        )
        comment_queryset = review.comments.all()
        return comment_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs['title_id']
        )
        author = self.request.user
        serializer.save(author=author, review=review)