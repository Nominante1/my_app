from django.http import HttpResponse
from .forms import SportForm
from django.shortcuts import render, redirect

# Create your views here.
def sport_view(request):
    if request.method == 'POST':
        form = SportForm(request.POST)
    else:
        form = SportForm()
    return render(request, 'lab_4/main.html', {'form': form})
