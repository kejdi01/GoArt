from rest_framework import viewsets, permissions

from application.artworks.models import Artwork, Category, Collection
from application.artworks.serializers import ArtworkSerializer, CategorySerializer, CollectionSerializer
from application.core.permissions import IsAuthorOrReadOnly


class ArtworkViewSet(viewsets.ModelViewSet):
    queryset = Artwork.objects.filter(is_public=True).order_by("-created_at")
    serializer_class = ArtworkSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.filter(is_public=True).order_by("-created_at")
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'