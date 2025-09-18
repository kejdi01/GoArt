from django.urls import include, path
from rest_framework.routers import DefaultRouter

from application.profiles.views import ProfileViewSet

app_name = 'profiles'

router = DefaultRouter()

router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]