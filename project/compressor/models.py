from django.db import models
from django.utils.text import slugify

from project.settings import AUTH_USER_MODEL


class Image(models.Model):
    image = models.ImageField(upload_to="upImage")
    slug = models.SlugField()
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name="Utilisateur", null=True)

    def __str__(self):
        return f"{self.user}{self.slug}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.image.name)
        super().save(*args, **kwargs)
