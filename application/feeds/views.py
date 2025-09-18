from rest_framework import generics
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated

from application.artworks.models import Artwork
from application.feeds.serializers import ArtworkFeedSerializer


class FollowingFeedPagination(CursorPagination):
    page_size = 10
    ordering = ('-created_at',)

class FollowingFeedAPIView(generics.ListAPIView):
    serializer_class = ArtworkFeedSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = FollowingFeedPagination

    def get_queryset(self):
        user_profile = self.request.user.profile
        following_profiles_ids = user_profile.followings.values_list('following_id', flat=True)

        queryset = Artwork.objects.filter(
            author__id__in=following_profiles_ids,
            is_public=True,
        )

        return queryset.select_related('author__user').prefetch_related("images")