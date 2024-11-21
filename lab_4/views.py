from django.http import HttpResponse
from .forms import SportForm
from .forms import DocumentForm, SportListForm, GENDERS, SPORT_CATEGORIES, SPORT_TYPES
from django.shortcuts import render, redirect, get_object_or_404
from .models import Document, Sportspeople
from django.conf import settings
import os
import json
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import IntegrityError


def sport_view(request):
    if request.method == 'POST':
        form = SportForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data 
            savepl = data.pop('savepl')  # извлекает и удаляет значения с ключами 'savepl' из формы
            if savepl == '1':
                save_sportspeople_data(data)
                messages.success(request, 'Данные успешно сохранены в JSON файл.')  # Добавлено сообщение об успешном сохранении
                form = SportForm()  # Создаем новый экземпляр формы
                return render(request, 'lab_4/main.html', {'form': form})
            elif savepl == '2':
                name = data['name']
                surname = data['surname']
                age = data['age']
                gender = dict(GENDERS).get(data['gender'], data['gender'])#добавляем не ключи, а значения
                spcat = dict(SPORT_CATEGORIES).get(data['spcat'])
                sptype = ', '.join([dict(SPORT_TYPES).get(sptype) for sptype in data['sptype']]) #через запятую выводим значения, а не ключи
                sportsperson = Sportspeople(name=name, surname=surname, age=age, gender=gender, spcat=spcat, sptype=sptype)
                try:
                    sportsperson.save()
                except IntegrityError:
                    messages.error(request, 'Обнаружен дупликат')
                    return render(request, 'lab_4/main.html', {'form': form})
                messages.success(request, 'Данные успешно сохранены в базу данных.')  # Добавлено сообщение об успешном сохранении
                form = SportForm()  # Создаем новый экземпляр формы
                return render(request, 'lab_4/main.html', {'form': form})
    else:
        form = SportForm()  
    return render(request, 'lab_4/main.html', {'form': form})

def save_sportspeople_data(data):
    folder_path = os.path.join(settings.BASE_DIR, 'Sportspeople')  # создаём путь для папки с json
    os.makedirs(folder_path, exist_ok=True)  # создаём папку, если её нет

    file_path = os.path.join(folder_path, 'sportspeople.json')  # если файл существует, формируем путь до него
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)  # если файла нет, создаём его как список

    with open(file_path, 'r+') as f:  # открываем файл json
        file_content = f.read().strip()  # чтение без пробелов
        if file_content:  # если файл не пуст (иначе при пустом файле будет выдавать ошибку декодирования)
            f.seek(0)  # возвращаем курсор в начало файла
            sportspeople = json.load(f)  # загружаем данные из файла в переменную
        else:
            sportspeople = []  # если файл пустой, добавляем пустой список
        sportspeople.append(data)  # добавляем в список данные, полученные как аргумент
        f.seek(0)  # переносим курсор в начало строки
        json.dump(sportspeople, f, ensure_ascii=False, indent=4)  # добавляем информацию из переменной в файл f
        
def sportperson_list(request):
    sportspeople = []  # Инициализируем переменную перед использованием
    if request.method == 'POST':
        form = SportListForm(request.POST)
        if form.is_valid():
            readpl = form.cleaned_data['readpl']
            if readpl == '1':
                file_path = os.path.join(settings.BASE_DIR, 'Sportspeople', 'sportspeople.json')
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        file_content = f.read().strip()
                        if file_content:
                            f.seek(0)
                            sportspeople = json.load(f)
                        else:
                            sportspeople = []
            elif readpl == '2':
                sportspeople = list(Sportspeople.objects.all().values())
            return render(request, 'lab_4/sportperson_list.html', {'sportspeople': sportspeople, 'form': form, 'readpl': readpl})
    else:
        form = SportListForm()
        sportspeople = []
    return render(request, 'lab_4/sportperson_list.html', {'sportspeople': sportspeople, 'form': form})

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


def get_sportperson(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            sportperson = list(Sportspeople.objects.all().values())
            return JsonResponse({'context': sportperson})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
       return HttpResponseBadRequest('Invalid request')

def find_sportperson(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            query = request.GET.get('q', '').strip()#получаем строку, ищем значение q
            if query:
                sportperson = list(
                    Sportspeople.objects.filter(name__icontains=query).values() | 
                    Sportspeople.objects.filter(surname__icontains=query).values()
                    ) #Проверка, включают ли поля формы введённую строку   
            else:
                sportperson = list(Sportspeople.objects.all().values())#если ничего не введено, вывести все записи
            return JsonResponse({'context': sportperson})
    return JsonResponse({'status': 'Invalid request'}, status=400)

#функция для редактирования

def edit_sp_temp(request):
    return render(request, 'lab_4/edit_sportperson.html')

def edit_sportperson(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            record_id = request.GET.get('id', '').strip()
            new_spcat = request.GET.get('input', '').strip()
            if record_id and new_spcat:
                s = ".,:;!_*-+()/#%&"
                for char in s:
                    if char in new_spcat:
                        return JsonResponse({'status': 'Incorrect sport category'}, status=400) 
                sportperson = Sportspeople.objects.filter(pk=record_id).update(spcat=new_spcat)
                sportperson = Sportspeople.objects.get(pk=record_id)
                sportperson_data = {
                        'id': sportperson.pk,
                        'name': sportperson.name,
                        'surname': sportperson.surname,
                        'age': sportperson.age,
                        'gender': sportperson.gender,
                        'spcat': sportperson.spcat,
                        'sptype': sportperson.sptype,
                    }
                return JsonResponse({'status': 'Success', 'sportperson': sportperson_data})
    return JsonResponse({'status': 'Invalid request'}, status=400)
                
def delete_sportperson(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            record_id = request.GET.get('id', '').strip()
            if record_id:
                sportperson = get_object_or_404(Sportspeople, pk=record_id)
                sportperson.delete()
                sportperson = list(Sportspeople.objects.all().values())
                return JsonResponse({'status': 'Success', 'context': sportperson})
    return JsonResponse({'status': 'Invalid request'}, status=400)   


#def edit_sportperson(request, pk):
#    sportsperson = get_object_or_404(Sportspeople, pk=pk)
#    
    # Передаем только спортивную категорию для редактирования
#   if request.method == 'POST':
#        form = SportForm(request.POST, instance=sportsperson)
#        
#        if form.is_valid():
#            # Сохраняем только изменение спортивной категории
#            form.save()
#            messages.success(request, 'Спортивная категория успешно обновлена.')
#            return redirect('sportperson_list')  # Перенаправляем на список спортсменов
#    else:
#        form = SportForm(instance=sportsperson)
#
#    return render(request, 'lab_4/edit_sportperson.html', {'form': form})

#def get_sportperson_for_updating(request, id):
#    sportperson = get_object_or_404(Sportspeople, id=id)
#    return JsonResponse({
#        'name': sportperson.name,
#        'surname': sportperson.surname,
#        'age': sportperson.age,
#        'gender': sportperson.gender,
#        'spcat': sportperson.spcat,
#        'sptype': sportperson.sptype,
#    })
