from django import forms
from .models import UpImage


class UploadImage(forms.ModelForm):

    class Meta:
        model = UpImage
        fields = ["image"]


class Compress(forms.Form):
    quality = forms.IntegerField(label="Qualité")
    width = forms.IntegerField(label="Largeur")
    height = forms.IntegerField(label="Hauteur")
