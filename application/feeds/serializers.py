from rest_framework import serializers

from application.artworks.models import ArtworkImage, Artwork
from application.profiles.models import Profile


class AuthorFeedSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "username"]

class ArtworkImageFeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtworkImage
        fields = ["id", "image"]

class ArtworkFeedSerializer(serializers.ModelSerializer):
    author = AuthorFeedSerializer(read_only=True)
    image = ArtworkImageFeedSerializer(read_only=True)

    class Meta:
        model = Artwork
        fields = ["id", "slug", "title", "author", "description", "image", "created_at"]