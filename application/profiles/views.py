from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from application.profiles.models import Profile, Follow
from application.profiles.serializers import ProfileSummarySerializer


class ProfileViewSet(ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSummarySerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    @action(detail=True, methods=['POST'])
    def follow(self, request, pk=None):
        profile_to_follow = get_object_or_404(Profile, pk=pk)
        follower_profile = request.user.profile

        if follower_profile == profile_to_follow:
            return Response({'message': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(follower=follower_profile, following=profile_to_follow).exists():
            return Response({"error": "You are already following this profile."}, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.create(follower=follower_profile, following=profile_to_follow)

        return Response({"status": "followed"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def unfollow(self, request, pk=None):
        profile_to_unfollow = get_object_or_404(Profile, pk=pk)
        follower_profile = request.user.profile

        follow_instance = Follow.objects.filter(follower=follower_profile, following=profile_to_unfollow)

        if not follow_instance.exists():
            return Response({"error": "You are not following this profile."}, status=status.HTTP_400_BAD_REQUEST)

        follow_instance.delete()

        return Response({"status": "unfollowed"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def followers(self, request, pk=None):
        profile = self.get_object()
        follower_ids = profile.followers.values_list('follower_id', flat=True)
        followers_queryset = Profile.objects.filter(id__in=follower_ids)

        page = self.paginate_queryset(followers_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(followers_queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        profile = self.get_object()
        following_ids = profile.followings.values_list('following_id', flat=True)
        following_queryset = Profile.objects.filter(id__in=following_ids)

        page = self.paginate_queryset(following_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(following_queryset, many=True)
        return Response(serializer.data)

