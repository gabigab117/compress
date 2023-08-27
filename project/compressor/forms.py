from django import forms
from .models import UpImage


# Formulaire basique
class UploadImage(forms.ModelForm):

    class Meta:
        model = UpImage
        fields = ["image"]


# Non premium
class Compress(forms.Form):
    quality = forms.IntegerField(label="Qualité")
    width = forms.IntegerField(label="Largeur", required=False)
    height = forms.IntegerField(label="Hauteur", required=False)


class PremiumForm(forms.ModelForm):
    quality = forms.IntegerField(label="Qualité")
    width = forms.IntegerField(label="Largeur", required=False)
    height = forms.IntegerField(label="Hauteur", required=False)

    class Meta:
        fields = ["quality", "width", "height"]
