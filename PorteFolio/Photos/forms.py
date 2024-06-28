from django import forms
from django.forms import ClearableFileInput

from . import models


class PhotoForm(forms.ModelForm):
    thumbnail = forms.ImageField(widget=ClearableFileInput(attrs={'multiple': False}),required=False)

    class Meta:
        model = models.Photo
        fields = ['title', 'description', 'image', 'thumbnail']


class DeleteForm(forms.Form):
    delete = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    photo_id = forms.IntegerField(widget=forms.HiddenInput())
