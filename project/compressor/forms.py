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
    quality = forms.IntegerField(label="Qualité", min_value=1, max_value=95, required=True)
    width = forms.IntegerField(label="Largeur", required=False)
    height = forms.IntegerField(label="Hauteur", required=False)

    class Meta:
        model = UpImage
        fields = ["quality", "width", "height"]


class PremiumDeleteForm(forms.ModelForm):
    delete = forms.BooleanField(initial=False, required=False, label="Supprimer")

    class Meta:
        model = UpImage
        fields = ["delete"]

    def save(self, *args, **kwargs):
        if self.cleaned_data["delete"]:
            self.instance.delete()
            return True
        return super().save(*args, **kwargs)
