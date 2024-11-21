from django.db import models

class Document(models.Model): #модель, определяющая то, какой информацией будет сопровождаться загруженный документ
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')  # Путь, куда сохраняются файлы
    uploaded_at = models.DateTimeField(auto_now_add=True)
# Create your models here.

class Sportspeople(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    spcat = models.CharField(max_length=100)
    sptype = models.TextField()  # Используем TextField для хранения нескольких значений
#    savepl = models.CharField(max_length=100)  # Добавляем поле для хранения места сохранения
    class Meta:
        unique_together = ('name', 'surname', 'age', 'gender', 'spcat', 'sptype')
