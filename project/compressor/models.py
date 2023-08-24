from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from project.settings import AUTH_USER_MODEL

from PIL import Image
import datetime


class UpImage(models.Model):
    image = models.ImageField(upload_to="upImage")
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name="Utilisateur", null=True, blank=True)
    published = models.DateField(null=True)
    expire = models.DateField(null=True)

    def __str__(self):
        return f"{self.user} - {self.published}"

    def save(self, *args, **kwargs):
        if not self.published:
            self.published = timezone.now()
        self.expire = self.published + timezone.timedelta(days=1)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('compressor:image', kwargs={"pk": self.pk})

    def get_extension(self):
        split_name = self.image.name.split(".")
        ext = split_name[-1]
        if ext == "jpg":
            return "JPEG"
        return ext

    def adjust_file_name(self):
        file_name = self.image.name
        split_name = file_name.split("/")
        new_name = split_name[-1]
        return new_name
