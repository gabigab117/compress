from django import forms
from .models import UpImage


class UploadImage(forms.ModelForm):
    width = forms.IntegerField(label="Largeur", required=False)
    height = forms.IntegerField(label="Hauteur", required=False)
    quality = forms.IntegerField(label="Qualité", required=False)

    class Meta:
        model = UpImage
        fields = ["image"]
