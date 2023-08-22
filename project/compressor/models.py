from django.db import models
from django.utils.text import slugify

from project.settings import AUTH_USER_MODEL

from PIL import Image
import string
import random


class UpImage(models.Model):
    image = models.ImageField(upload_to="upImage")
    slug = models.SlugField()
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name="Utilisateur", null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.slug}"

    def random_name(self):
        letters = string.ascii_lowercase
        random_name = random.choices(letters, k=50)
        random_name = "".join(random_name)
        split_name = self.image.name.split(".")
        new_name = random_name + "." + str(split_name[-1])
        return new_name

    def save(self, *args, **kwargs):
        # self.image.name = self.random_name()
        if not self.slug:
            self.slug = slugify(self.image.name)
        super().save(*args, **kwargs)
