from rest_framework import serializers

from application.artworks.models import ArtworkImage, Artwork, Collection, Category


class ArtworkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkImage
        fields = '__all__'

class ArtworkSerializer(serializers.ModelSerializer):
    images = ArtworkImageSerializer(many=True, read_only=True)

    class Meta:
        model = Artwork
        fields = '__all__'
        lookup_field = 'slug'

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'