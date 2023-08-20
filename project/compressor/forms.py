from django import forms
from .models import Image


class UploadImage(forms.ModelForm):
    width = forms.IntegerField(label="Largeur")
    height = forms.IntegerField(label="Hauteur")

    class Meta:
        model = Image
        fields = ["image"]
