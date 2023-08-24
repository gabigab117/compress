from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from .models import UpImage
from .forms import UploadImage, Compress
from PIL import Image

from io import BytesIO


def index(request):
    if request.method == "POST":
        form = UploadImage(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()

            return redirect("compressor:image", pk=image.pk)
    else:
        form = UploadImage()
    return render(request, "compressor/index.html", context={"form": form})


def image_view(request, pk):
    my_image = UpImage.objects.get(pk=pk)
    if request.method == "POST":
        form = Compress(request.POST)
        if form.is_valid():
            # commencer par gérer que la qualité
            quality = form.cleaned_data["quality"]
            width = form.cleaned_data["width"]
            height = form.cleaned_data["height"]
            if quality:
                image = Image.open(my_image.image)
                if width and height:
                    image.thumbnail((width, height))
                im_io = BytesIO()
                ext = my_image.get_extension()
                image.save(im_io, ext.upper(), quality=quality)
                # ajuste pour ne pas créer des sous dossiers
                file_name = my_image.adjust_file_name()
                my_image.image.delete()
                my_image.image.save(file_name, ContentFile(im_io.getvalue()), save=False)
                my_image.save()
                return redirect(my_image)

    else:
        form = Compress()
    return render(request, "compressor/image.html", context={"image": my_image, "form": form})


def premium_upload(request):
    user = request.user

    if request.method == "POST":
        data = request.POST
        images = request.FILES.getlist("images")
        print(images)
        print(data)
        for image in images:
            up_image = UpImage.objects.create(image=image, user=user)
        return redirect("index")

    return render(request, "compressor/premium.html")
