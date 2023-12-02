from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import CustomUser

from .models import UpImage
from .forms import UploadImage, Compress, PremiumForm, PremiumDeleteForm
from project.settings import STRIPE_KEY, STRIPE_PRICE_ID

import stripe
import os

stripe.api_key = STRIPE_KEY


def index(request):
    if request.method == "POST":
        form = UploadImage(request.POST, request.FILES)

        if form.is_valid():
            image = form.save(commit=False)

            exclude = image.format_exclusion(request)
            if exclude:
                return redirect("index")

            if request.user.is_authenticated:
                image.user = request.user
                if image.user_has_subscription():
                    image.archived = True

            image.save()

            return redirect("compressor:image", pk=image.pk)
    else:
        form = UploadImage()
    return render(request, "compressor/index.html", context={"form": form})


def image_view(request, pk):
    my_image = UpImage.objects.get(pk=pk)

    if request.method == "POST":
        form = Compress(request.POST)
        if form.is_valid():
            quality = form.cleaned_data["quality"]
            width = form.cleaned_data["width"]
            height = form.cleaned_data["height"]

            my_image.compress_image(quality, width, height)
            return redirect(my_image)

    else:
        form = Compress()
    return render(request, "compressor/image.html", context={"image": my_image, "form": form})


def user_has_sub(user):
    if user.stripe_sub_id:
        subscription = stripe.Subscription.retrieve(user.stripe_sub_id)
        return subscription.status == "active"
    return False


@user_passes_test(user_has_sub, login_url="compressor:subscription")
def premium_upload(request):
    user = request.user

    if request.method == "POST":
        images = request.FILES.getlist("images")
        quality = request.POST.get("quality")
        width = request.POST.get("width")
        height = request.POST.get("height")

        for image in images:
            my_image = UpImage.objects.create(image=image, user=user)

            exclude = my_image.format_exclusion(request)
            if exclude:
                my_image.delete()
                continue

            if quality:
                my_image.compress_image(int(quality), width, height)
                my_image.archive_image()

        if quality:
            return redirect("compressor:all-premium-images")
        return redirect("compressor:premium-images")

    return render(request, "compressor/premium.html")


@user_passes_test(user_has_sub, login_url="compressor:subscription")
def premium_images_view(request):
    user = request.user
    images = UpImage.objects.filter(user=user, archived=False)

    UpFormSet = modelformset_factory(UpImage, form=PremiumForm, extra=0)
    formset = UpFormSet(queryset=images)

    if request.method == "POST":
        formset = UpFormSet(request.POST, queryset=images)

        if formset.is_valid():
            for form in formset:
                quality = form.cleaned_data["quality"]
                width = form.cleaned_data["width"]
                height = form.cleaned_data["height"]
                my_image = form.instance

                my_image.compress_image(quality, width, height)
                my_image.archive_image()

            return redirect("compressor:all-premium-images")

    return render(request, "compressor/images-premium.html", context={"forms": formset})


@user_passes_test(user_has_sub, login_url="compressor:subscription")
def all_premium_images(request):
    user = request.user
    images = UpImage.objects.filter(user=user, archived=True)
    DelFormSet = modelformset_factory(UpImage, form=PremiumDeleteForm, extra=0)
    formset = DelFormSet(queryset=images)

    if request.method == "POST":
        formset = DelFormSet(request.POST, queryset=images)
        if formset.is_valid:
            formset.save()
            return redirect("compressor:all-premium-images")

    return render(request, "compressor/all-images.html", context={"images": images, "forms": formset})


@login_required
def subscription_view(request):
    user = request.user

    if user.stripe_sub_id:
        subscription = stripe.Subscription.retrieve(user.stripe_sub_id)
        product = stripe.Product.retrieve(subscription.plan.product)
        return render(request, "compressor/subscription.html", context={'subscription': subscription,
                                                                        'product': product})

    else:
        return render(request, "compressor/subscription.html")


def create_checkout_session(request):
    checkout_data = {
        "locale": "fr",
        "line_items": [{'price': STRIPE_PRICE_ID, 'quantity': 1}],
        "mode": 'subscription',
        "shipping_address_collection": {"allowed_countries": ["FR", "BE"]},
        "success_url": request.build_absolute_uri(reverse("compressor:checkout-success")),
        "cancel_url": 'http://127.0.0.1:8000'}

    if request.user.stripe_id:
        checkout_data["customer"] = request.user.stripe_id
    else:
        checkout_data["customer_email"] = request.user.email

    session = stripe.checkout.Session.create(**checkout_data)

    return redirect(session.url, code=303)


def checkout_success(request):
    return render(request, "compressor/success.html")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    # Penser à renseigner une clé pour la prod
    endpoint_secret = os.environ.get("endpoint_secret")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'checkout.session.completed':
        data = event['data']['object']

        user = get_object_or_404(CustomUser, email=data['customer_details']['email'])

        if not user.stripe_id:
            user.stripe_id = data["customer"]
            user.save()

        user.stripe_sub_id = data["subscription"]
        user.save()

    return HttpResponse(status=200)
