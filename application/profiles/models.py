from django.db import models

from project import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followings')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.user.email} follows {self.following.user.email}"
    class Meta:
        unique_together = ('follower', 'following')
