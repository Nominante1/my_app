from django import forms
from django.core.exceptions import ValidationError
from .models import Document, Sportspeople
import json

SPORT_CATEGORIES = [
    ('candidate', 'Кандидат в мастера спорта'),
    ('first', 'Первый спортивный разряд'),
    ('second', 'Второй спортивный разряд'),
    ('third', 'Третий спортивный разряд'),
    ('junior_first', 'Первый юношеский спортивный разряд'),
    ('junior_second', 'Второй юношеский спортивный разряд'),
    ('junior_third', 'Третий юношеский спортивный разряд')
]
GENDERS = [('man', 'Мужчина'), ('woman', 'Женщина')]
SPORT_TYPES = [
    ('hockey', 'Хоккей'),
    ('football', 'Футбол'),
    ('skating', 'Фигруное катание'),
    ('biathlon', 'Биатлон'),
    ('boxing', 'Бокс'),
    ('other', 'Другое'),
]
SAVINGPLACE = [(1, 'JSON'), (2, 'DB')]

class SportForm(forms.ModelForm):
    class Meta:
        model = Sportspeople
        fields = ['name', 'surname', 'age', 'gender', 'spcat', 'sptype']#'savepl'

    name = forms.CharField(widget=forms.TextInput, label="Имя")
    surname = forms.CharField(widget=forms.TextInput, label="Фамилия")
    age = forms.IntegerField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 10}), label="Возраст", min_value=1, max_value=100)
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDERS, label="Пол")
    spcat = forms.ChoiceField(choices=SPORT_CATEGORIES, label="Спортивная категория")
    sptype = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=SPORT_TYPES,
        label="Виды спорта"
    )
    savepl = forms.ChoiceField(choices=SAVINGPLACE, label="Сохранить в...")
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        surname = cleaned_data.get('surname')
        age = cleaned_data.get('age')
        gender = cleaned_data.get('gender')
        spcat = cleaned_data.get('spcat')
        sptype = cleaned_data.get('sptype')

        # Преобразуем список sptype в строку, разделенную запятыми
        sptype = ",".join(sorted(sptype))  # Строка типов спорта для поиска дубликатов

        # Проверяем наличие дубликата в базе данных
        if Sportspeople.objects.filter(
            name=name, 
            surname=surname, 
            age=age, 
            gender=gender, 
            spcat=spcat, 
            sptype=sptype
            ).exists():
            raise ValidationError("Спортсмен с такими данными уже существует.")
        return cleaned_data

READINGPLACE = [(1, 'JSON'), (2, 'DB')]

class SportListForm(forms.Form):
    readpl = forms.ChoiceField(choices=READINGPLACE, label="Прочитать из...")

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)

    def clean_file(self):
        file = self.cleaned_data.get('file')
        print(file.name)
        # Проверяем расширение файла
        if not file.name.endswith('.json'):
            raise forms.ValidationError('Только файлы формата JSON допустимы.')
        try:
            # Читаем файл для проверки на JSON
            file_content = file.read().decode('utf-8')
            json.loads(file_content)
            file.seek(0)  # Возвращаем курсор в начало для последующего использования
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise forms.ValidationError('Файл не является валидным JSON.')
        return file

#def clean_file(self):
#     file = self.cleaned_data.get('file')
#     mime = magic.Magic(mime=True)
#     file_type = mime.from_buffer(file.read())
#     if not file_type.startswith('image/'):  # Например, только изображения
#         raise forms.ValidationError('Этот файл не является изображением.')
#     return file