from django.urls import path
from.views import image_view, premium_upload


app_name = "compressor"
urlpatterns = [
    path("image/<int:pk>/", image_view, name="image"),
    path("premium/", premium_upload, name="premium")
]
