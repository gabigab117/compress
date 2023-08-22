from django.contrib import admin
from django.urls import path, include
from project import settings
from django.conf.urls.static import static
from compressor.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
    path('compressor/', include("compressor.urls")),
    path('account/', include("accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
