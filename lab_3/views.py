from django.http import HttpResponse
from .forms import PasswordForm
from django.shortcuts import render, redirect
# Create your views here.
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
    return render(request, 'lab_3/main.html')
