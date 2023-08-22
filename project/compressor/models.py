from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from project.settings import AUTH_USER_MODEL

from PIL import Image


class UpImage(models.Model):
    image = models.ImageField(upload_to="upImage")
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name="Utilisateur", null=True, blank=True)

    def __str__(self):
        return f"{self.user}"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('compressor:image', kwargs={"pk": self.pk})

    def get_extension(self):
        split_name = self.image.name.split(".")
        ext = split_name[-1]
        return ext
