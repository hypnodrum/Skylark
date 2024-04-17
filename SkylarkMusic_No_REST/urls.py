from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from SkylarkMusic_No_REST import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('SkylarkMusic_No_REST.web.urls')),
    path("profile/", include('SkylarkMusic_No_REST.profiles.urls')),
    path("media/", include('SkylarkMusic_No_REST.audio_library.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
