from django.urls import include, path
<<<<<<< HEAD
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, register, get_jwt_token

v1_router = DefaultRouter()

v1_router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', register, basename='register'),
    path('v1/auth/token/', get_jwt_token, basename='token')
=======
from rest_framework.routers import SimpleRouter

from .views import CategoriesViewSet, GenreViewSet, TittleViewSet

router_v1 = SimpleRouter()
router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TittleViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
>>>>>>> 38b3ea384d31124ed2d2c877415de7fd2dd18116
]
