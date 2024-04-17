from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from .mixins import CustomURLField


class SkylarkUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(
        validators=(MinValueValidator(16),),
        help_text="Age requirement: 16 years and above.",
        null=True,
        blank=True,
    )
    country = models.CharField(max_length=60, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    bio = models.TextField(max_length=2000, blank=True, null=True)
    profile_picture = CustomURLField(blank=True, null=True)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.user.username


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')

    def __str__(self):
        return f'{self.subscriber} is following {self.user}'


class SocialLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_links')
    link = models.URLField(max_length=200)

    def __str__(self):
        return f'{self.link} social link of {self.user}'
