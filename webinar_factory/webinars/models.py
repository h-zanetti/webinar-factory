from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='nome')

    def __str__(self):
        return self.name

class Webinar(models.Model):
    name = models.CharField('nome do evento', max_length=150)
    description = models.TextField('descrição')
    timestamp_st = models.DateTimeField('início')
    timestamp_end = models.DateTimeField('fim')
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='organizador')
    tags = models.ManyToManyField(Tag)
    staff = models.ManyToManyField(User)

    def __str__(self):
        return self.name
