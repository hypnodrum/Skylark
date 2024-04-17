from django import forms
from django.db import models
from django.http import Http404
from SkylarkMusic_No_REST.profiles.custom_validators import validate_picture_format


def get_object_or_404(obj, request_user):
    if obj != request_user:
        raise Http404("You do not have permission to view this profile.")
    return obj


class CustomURLField(models.URLField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(validate_picture_format)


class CustomFormURLField(forms.URLField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(validate_picture_format)
