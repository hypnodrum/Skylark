from django.contrib import admin
from . import models


@admin.register(models.SkylarkUser)
class SkylarkUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'age', 'country', 'city','bio', 'profile_picture',)
    list_display_links = ('id',)


@admin.register(models.Follower)
class SocialFollowerAdmin(admin.ModelAdmin):
    list_display = ('user','subscriber',)


@admin.register(models.SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('user','link',)
