from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # Local urls
    path('', include('accounts.urls', namespace='accounts')),
    path('', include('home.urls', namespace='home')),
    path('video/', include('video.urls', namespace='video')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
