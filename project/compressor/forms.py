from django import forms
from .models import Image


class UploadImage(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image"]
