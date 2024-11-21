from django.urls import path
from .views import sport_view, upload_file, file_list, sportperson_list, get_sportperson, find_sportperson, edit_sp_temp, edit_sportperson, delete_sportperson

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('mainsport/', sport_view, name='sport_view'),
        path('upload/', upload_file, name='upload_file'),
        path('files/', file_list, name='file_list'),
        path('sportsperson/', sportperson_list, name='splist'),
        path('get_sportperson/', get_sportperson, name='get_sportperson'),
        path('find_sportperson/', find_sportperson, name='find_sportperson'),
        path('edit_sportperson/', edit_sportperson, name='edit_sportperson'),
        path('edit_sp_temp/', edit_sp_temp, name='edit_sp_temp'),
        path('delete_sportperson/', delete_sportperson, name='delete_sportperson'),
    ]
if settings.DEBUG: #во время разработки мы получаем новый маршрут: /localhost8000/media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)