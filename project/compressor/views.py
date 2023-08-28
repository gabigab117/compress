from django.core.files.base import ContentFile
from django.forms import modelformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from .models import UpImage
from .forms import UploadImage, Compress, PremiumForm
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
        quality = request.POST.get("quality")
        width = request.POST.get("width")
        height = request.POST.get("height")
        for image in images:
            my_image = UpImage.objects.create(image=image, user=user)
            if quality:
                quality = int(quality)
                image = Image.open(my_image.image)

                if width and height:
                    width = int(width)
                    height = int(height)
                    image.thumbnail((width, height))

                im_io = BytesIO()
                ext = my_image.get_extension()
                image.save(im_io, ext.upper(), quality=quality)
                # ajuste pour ne pas créer des sous dossiers
                file_name = my_image.adjust_file_name()
                my_image.image.delete()
                my_image.image.save(file_name, ContentFile(im_io.getvalue()), save=False)
                my_image.archived = True
                my_image.save()

        if quality:
            return redirect("compressor:all-premium-images")
        return redirect("compressor:premium-images")

    return render(request, "compressor/premium.html")


def premium_images_view(request):
    user = request.user
    images = UpImage.objects.filter(user=user, archived=False)
    # Je crée une classe depuis le formsetfactory
    UpFormSet = modelformset_factory(UpImage, form=PremiumForm, extra=0)
    formset = UpFormSet(queryset=images)
    return render(request, "compressor/images-premium.html", context={"forms": formset})


def compress_images_premium(request):
    if request.method != "POST":
        raise Http404("Requête invalide")

    user = request.user
    images = UpImage.objects.filter(user=user, archived=False)
    UpFormSet = modelformset_factory(UpImage, form=PremiumForm, extra=0)
    formset = UpFormSet(request.POST, queryset=images)

    if formset.is_valid():

        for form in formset:
            quality = form.cleaned_data["quality"]
            width = form.cleaned_data["width"]
            height = form.cleaned_data["height"]
            my_image = form.instance
            image = Image.open(form.instance.image)
            if width and height:
                image.thumbnail((width, height))
            im_io = BytesIO()
            ext = my_image.get_extension()
            image.save(im_io, ext.upper(), quality=quality)
            # ajuste pour ne pas créer des sous dossiers
            file_name = my_image.adjust_file_name()
            my_image.image.delete()
            my_image.image.save(file_name, ContentFile(im_io.getvalue()), save=False)
            my_image.archived = True
            my_image.save()

    return redirect("compressor:all-premium-images")


def all_premium_images(request):
    user = request.user
    images = UpImage.objects.filter(user=user, archived=True)
    return render(request, "compressor/all-images.html", context={"images": images})
