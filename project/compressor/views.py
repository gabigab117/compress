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
            image = form.save()

            return redirect("compressor:image", pk=image.pk)
    else:
        form = UploadImage()
    return render(request, "compressor/upimage.html", context={"form": form})


def image_view(request, pk):
    image = UpImage.objects.get(pk=pk)
    return render(request, "compressor/image.html", context={"image": image})
