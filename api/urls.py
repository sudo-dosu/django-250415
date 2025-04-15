from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CityViewSet, IDCViewSet, HostViewSet, ping_host

app_name = 'api'


router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='cities')
router.register(r'idcs', IDCViewSet, basename='idcs')
router.register(r'hosts', HostViewSet, basename='hosts')

urlpatterns = [
    path('', include(router.urls)),
    path('ping/<int:pk>/', ping_host),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
