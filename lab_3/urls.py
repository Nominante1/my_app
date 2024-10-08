from django.urls import path
from .views import password_view
from .views import main_page

urlpatterns = [
    path('password/', password_view, name='password_view'),
    path('main/', main_page, name='main_page'),
]
