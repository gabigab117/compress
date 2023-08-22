from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import UpImage
from .forms import UploadImage
from PIL import Image

import os


def index(request):
    return render(request, "compressor/index.html")


def up_image(request):
    if request.method == "POST":
        form = UploadImage(request.POST, request.FILES)
        if form.is_valid():
            quality = form.cleaned_data["quality"]
            image = form.save(commit=False)
            compress_image = Image.open(image.image)
            compressed_path = os.path.join("mediafiles/upImage", image.image.name)
            compress_image.save(f"{compressed_path}", optimize=True, quality=quality)
            image.image = compressed_path
            image.save()

            return redirect("compressor:upimage")
    else:
        form = UploadImage()
    return render(request, "compressor/upimage.html", context={"form": form})
