from django import forms

from .models import IFCFile


class IfcFileForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = IFCFile
        fields = ['file']
