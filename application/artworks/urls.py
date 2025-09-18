from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArtworkViewSet, CollectionViewSet, CategoryViewSet

app_name = 'artworks'
router = DefaultRouter()

router.register(r'artworks', ArtworkViewSet, basename='artwork')
router.register(r'collections', CollectionViewSet, basename='collection')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
