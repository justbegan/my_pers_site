from django.db import models

# Create your models here.


class Progress_bar(models.Model):
    all = models.IntegerField("Всего",default=0, max_length=100)
    current = models.IntegerField("На данный момент",default=0, max_length=100)
    status = models.BooleanField("Статус",default=True)