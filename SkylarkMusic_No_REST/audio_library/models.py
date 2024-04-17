from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import F
from SkylarkMusic_No_REST.audio_library.mixins import get_path_upload_track, get_path_upload_cover_track
from SkylarkMusic_No_REST.audio_library.validators import validate_size_image


class License(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='licenses')
    text = models.TextField(max_length=1000)


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    private = models.BooleanField(default=False)
    cover = models.URLField(
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif',]),]
    )


class Track(models.Model):
    TrackGenreHouse = "House"
    TrackGenreDance = "Dance"
    TrackGenreTrance = "Trance"
    TrackGenreRock = "Rock"
    TrackGenrePop = "Pop"

    CHOICES = (
        (TrackGenreHouse, TrackGenreHouse),
        (TrackGenreDance, TrackGenreDance),
        (TrackGenreTrance, TrackGenreTrance),
        (TrackGenreRock, TrackGenreRock),
        (TrackGenrePop, TrackGenrePop),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audio_library')
    title = models.CharField(max_length=100)
    license = models.ForeignKey(License, on_delete=models.PROTECT, related_name='license_tracks', null=True, blank=True)
    genre = models.CharField(max_length=10, choices=CHOICES, blank=False, null=False, default=None)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    link_of_author = models.CharField(max_length=500, blank=True, null=True)
    file = models.FileField(
        upload_to=get_path_upload_track,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])]
    )
    create_at = models.DateTimeField(auto_now_add=True)
    plays_count = models.PositiveIntegerField(default=0)
    download = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    user_of_likes = models.ManyToManyField(User, related_name='likes_of_tracks')
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to=get_path_upload_cover_track,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', ]), validate_size_image]
    )

    def increase_play_count(self):
        self.plays_count += 1
        self.save(update_fields=['plays_count'])

    def increase_download_count(self):
        self.download += 1
        self.save(update_fields=['download'])

    def increase_likes_count(self, user):
        self.likes_count = F('likes_count') + 1
        self.save(update_fields=['likes_count'])
        self.user_of_likes.add(user)

    def __str__(self):
        return f'{self.user} - {self.title}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='track_comments')
    text = models.TextField(max_length=1000)
    create_at = models.DateTimeField(auto_now_add=True)


class PlayList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='play_lists')
    title = models.CharField(max_length=50)
    tracks = models.ManyToManyField(Track, related_name='track_play_lists', blank=True, null=True)
    cover = models.URLField(
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif',]),]
    )
