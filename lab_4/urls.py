from django.urls import path
from .views import sport_view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('mainsport/', sport_view, name='sport_view'),
    ]
if settings.DEBUG: #во время разработки мы получаем новый маршрут: /localhost8000/media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)