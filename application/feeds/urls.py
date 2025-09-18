from django.urls import path
from .views import FollowingFeedAPIView

app_name = 'feeds'

urlpatterns = [
    path('following/', FollowingFeedAPIView.as_view(), name='following-feed'),
]