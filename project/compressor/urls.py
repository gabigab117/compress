from django.urls import path
from .views import (image_view, premium_upload, premium_images_view, all_premium_images,
                    subscription_view, create_checkout_session, checkout_success, stripe_webhook)

app_name = "compressor"
urlpatterns = [
    path("image/<int:pk>/", image_view, name="image"),
    path("premium/", premium_upload, name="premium"),
    path("premium-images/", premium_images_view, name="premium-images"),
    path("all-images/", all_premium_images, name="all-premium-images"),
    path("subscription/", subscription_view, name="subscription"),
    path("create-checkout-session/", create_checkout_session, name="create-checkout-session"),
    path("stripe-webhook/", stripe_webhook, name="stripe-webhook"),
    path("success/", checkout_success, name="checkout-success"),
]
