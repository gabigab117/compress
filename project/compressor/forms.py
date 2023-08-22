from django import forms
from .models import UpImage


class UploadImage(forms.ModelForm):

    class Meta:
        model = UpImage
        fields = ["image"]
