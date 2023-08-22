from django.urls import path
from.views import up_image, image_view


app_name = "compressor"
urlpatterns = [
    path("upimage/", up_image, name="upimage"),
    path("image/<int:pk>/", image_view, name="image"),
]
