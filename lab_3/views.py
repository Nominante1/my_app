from django.http import HttpResponse
from .forms import PasswordForm
from django.shortcuts import render
# Create your views here.
def password_view(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            # Здесь можно обработать валидный пароль
            return render(request, 'lab_3/success.html')
    else:
        form = PasswordForm()
    return render(request, 'lab_3/password_form.html', {'form': form})
