from django import forms
from django.core.exceptions import ValidationError

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
    age = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 10}), label="Возраст")
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDERS, label="Пол")
    spcat = forms.ChoiceField(choices=SPORT_CATEGORIES, label="Спортивная категория")
    sptypes = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=SPORT_TYPES,
        label="Виды спорта"
    )

