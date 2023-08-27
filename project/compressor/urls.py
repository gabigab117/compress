from django.urls import path
from.views import image_view, premium_upload, premium_images_view, compress_images_premium, all_premium_images


app_name = "compressor"
urlpatterns = [
    path("image/<int:pk>/", image_view, name="image"),
    path("premium/", premium_upload, name="premium"),
    path("premium-images/", premium_images_view, name="premium-images"),
    path("compress-images-premium/", compress_images_premium, name="compress-images-premium"),
    path("all-images/", all_premium_images, name="all-premium-images")
]
