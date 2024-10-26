from django import forms
from django.core.exceptions import ValidationError
from .models import Document
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
GENDERS = [(1, 'Man'), (2, 'Woman')]
SPORT_TYPES = [
    ('hockey', 'Хоккей'),
    ('football', 'Футбол'),
    ('skating', 'Фигруное катание'),
    ('biathlon', 'Биатлон'),
    ('boxing', 'Бокс'),
    ('other', 'Другое'),
]
class SportForm(forms.Form):
    name = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), label="Имя")
    surname = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), label="Фамилия")
    age = forms.IntegerField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 10}), label="Возраст", min_value=1, max_value=100)
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDERS, label="Пол")
    spcat = forms.ChoiceField(choices=SPORT_CATEGORIES, label="Спортивная категория")
    sptypes = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=SPORT_TYPES,
        label="Виды спорта"
    )

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)

    def clean_file(self):
        file = self.cleaned_data.get('file')
        # Проверяем расширение файла
        if not file.name.endswith('.json'):
            raise forms.ValidationError('Только файлы формата JSON допустимы.')
        try:
            # Временно читаем файл для проверки на JSON
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