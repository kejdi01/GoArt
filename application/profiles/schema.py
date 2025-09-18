import graphene
from graphene_django import DjangoObjectType

from application.artworks.models import ArtworkImage, Artwork, Collection
from application.profiles.models import Profile, Follow
from application.user.models import CustomUser


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "date_joined")

class ArtworkImageType(DjangoObjectType):
    class Meta:
        model = ArtworkImage
        fields = ("id", "image", "is_cover")

class ArtworkType(DjangoObjectType):
    class Meta:
        model = Artwork
        fields = ["id", "title", "slug", "description", "status", "price", "is_public", "images"]

class CollectionType(DjangoObjectType):
    class Meta:
        model = Collection
        fields = ["id", "title", "is_public", "artworks"]

class ProfileType(DjangoObjectType):
    user = graphene.Field(UserType)
    follower_count = graphene.Int()
    following_count = graphene.Int()

    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "verified", "collections", "follower_count", "following_count"]

    def resolve_follower_count(self, info):
        return self.followers.count()

    def resolve_following_count(self, info):
        return self.followings.count()

class Query(graphene.ObjectType):
    profile = graphene.Field(ProfileType, id=graphene.ID(required=True))

    def resolve_profile(self, info, id):
        return Profile.objects.prefetch_related(
            "collections__artworks__images"
        ).get(id=id)
