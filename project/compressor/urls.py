from django.urls import path
from.views import up_image


app_name = "compressor"
urlpatterns = [
    path("upimage/", up_image, name="upimage"),
]
