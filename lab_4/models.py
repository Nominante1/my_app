from django.db import models

class Document(models.Model): #модель, определяющая то, какой информацией будет сопровождаться загруженный документ
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')  # Путь, куда сохраняются файлы
    uploaded_at = models.DateTimeField(auto_now_add=True)
# Create your models here.
