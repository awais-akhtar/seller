
from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("", include("myapp.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)