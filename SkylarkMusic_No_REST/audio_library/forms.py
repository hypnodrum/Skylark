from django import forms
from SkylarkMusic_No_REST.audio_library.models import Track


class CreateTrackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].help_text = ''
        self.fields['cover'].help_text = ''

    class Meta:
        model = Track
        fields = ['title', 'file', 'cover', 'private', 'genre', 'album']


class SearchForm(forms.Form):
    query = forms.CharField(label='Search')
