import logging #для отладки
from django.http import HttpResponse
from .forms import PasswordForm
from django.shortcuts import render, redirect

logger = logging.getLogger(__name__)

def password_view(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            # Здесь можно обработать валидный пароль
            return redirect('main_page')#перенаправление на основную страницу
    else:
        form = PasswordForm()
    return render(request, 'lab_3/password_form.html', {'form': form})

def main_page(request):
    theme = request.COOKIES.get('theme', 'light')  # По умолчанию 'light' если куки не установлены
    # Передаем тему в шаблон
    return render(request, 'lab_3/main.html', {'theme': theme})

def toggle_theme(request):
    # Переключаем тему
    if request.method == 'POST':
        current_theme = request.COOKIES.get('theme', 'light')
        logger.debug(f"Текущая тема: {current_theme}")
        if current_theme == 'light':
            new_theme = 'dark' 
        else:
            new_theme = 'light'
        # Устанавливаем новую тему в куки
        response = redirect('main_page')  # Переход к основной странице
        response.set_cookie('theme', new_theme, max_age=3600)  # Сохраняем куки на час
        return response
    return redirect('main_page')