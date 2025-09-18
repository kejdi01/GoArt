from rest_framework import serializers

from application.profiles.models import Profile


class ProfileSummarySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = [ "id", "username" ]
