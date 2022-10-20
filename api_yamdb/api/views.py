import django_filters
from django.core.mail import send_mail
from .permissions import (IsAdmin,
                         IsAdminOrReadOnly,
                         IsModeratorIsOwnerOrReadOnly)
from .serializers import (UserSerializer,
                          UserEditSerializer,
                          RegistraterUserSerializer,
                          TokenUserSerializer,
                          CommentSerializer,
                          RewiewSerializer,
                          CategoriesSerializer,
                          GenreSerializer,
                          ReadTittleSerializer,
                          TittleSerializer)
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters, mixins, viewsets, status, permissions
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from reviews.models import Categories, Genre, Title, Review, Comment, User


class CreateListDeleteViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                              mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass


class TitleFilter(FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    genre = django_filters.CharFilter(field_name='genre__slug')
    name = django_filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegistraterUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация',
        message=f'Токен для пользователя {user}: {confirmation_code}',
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer=TokenUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
            User,
        username=serializer.validated_data['username']
        )
    if default_token_generator.check_token(
        user,
            serializer.validated_data['confirmation_code']
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
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoriesViewSet(CreateListDeleteViewSet):
    lookup_field = 'slug'
    queryset = Categories.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )


class GenreViewSet(CreateListDeleteViewSet):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ReadTittleSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadTittleSerializer
        return TittleSerializer


class ReviewViewset(viewsets.ModelViewSet):
    serializer_class = RewiewSerializer
    permission_classes = [IsModeratorIsOwnerOrReadOnly]
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
    permission_classes = [IsModeratorIsOwnerOrReadOnly]
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
