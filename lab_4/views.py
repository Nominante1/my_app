from django.http import HttpResponse
from .forms import SportForm
from .forms import DocumentForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Document
from django.conf import settings
import os
import json

# Create your views here.
def sport_view(request):
    if request.method == 'POST':
        form = SportForm(request.POST)
        if form.is_valid():
            save_sportspeople_data(form.cleaned_data)
            return render(request, 'lab_4/main.html')
    else:
        form = SportForm()
    return render(request, 'lab_4/main.html', {'form': form})

def save_sportspeople_data(data):
    folder_path = os.path.join(settings.BASE_DIR, 'Sportspeople') #создаём путь для папки с json
    os.makedirs(folder_path, exist_ok=True) #создаём папку, если её нет

    file_path = os.path.join(folder_path, 'sportspeople.json') #если файл существует, формируем путь до него
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f) #если файла нет, создаём его как список

    with open(file_path, 'r+') as f: #открываем файл json
        file_content = f.read().strip() #чтение без пробелов
        if file_content:  # если файл не пуст (иначе при пустом файле будет выдавать ошибку декодирования)
            f.seek(0)  # возвращаем курсор в начало файла
            sportspeople = json.load(f)#загружаем данные из файла в переменную
        else:
            sportspeople = []  # если файл пустой, добавляем пустой список
        sportspeople.append(data) #добавляем в список данные, полученные как аргумент
        f.seek(0) #переносим курсор в начало строки???
        json.dump(sportspeople, f, ensure_ascii=False, indent=4)#добавляем информацию из переменной в файл f

def sportperson_list(request):
    file_path = os.path.join(settings.BASE_DIR, 'Sportspeople', 'sportspeople.json')
    sportspeople = []

    if os.path.exists(file_path): #если файл существует
        with open(file_path, 'r') as f:
            file_content = f.read().strip()
            if file_content:  # если файл не пуст
                f.seek(0)  # возвращаем курсор в начало файла
                sportspeople = json.load(f)  # загружаем данные
            else:
                sportspeople = []  # если файл пустой, оставляем список пустым
    return render(request, 'templates/lab_4/sportperson_list.html', {'sportspeople': sportspeople})

def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = DocumentForm()
    return render(request, 'lab_4/upload.html', {'form': form})

def file_list(request):
    file_dir = os.path.join(settings.MEDIA_ROOT, 'documents')
    json_files = []

    if os.path.exists(file_dir):
        for filename in os.listdir(file_dir):
            if filename.endswith('.json'):
                json_files.append(filename)
    context = {
        'json_files': json_files, #нужен как словарь для html (списки не пропускает)
    }
    return render(request, 'lab_4/file_list.html', context)


