from django.urls import include, path
from rest_framework.routers import SimpleRouter

router_v1 = SimpleRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]