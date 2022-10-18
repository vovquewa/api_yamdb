from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoriesViewSet, GenreViewSet, TittleViewSet

router_v1 = SimpleRouter()
router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TittleViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
