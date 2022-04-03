from django.db import models
from webinar_factory.users.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='nome')

    def __str__(self):
        return self.name

class Webinar(models.Model):
    name = models.CharField('nome', max_length=75)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='organizador', related_name='organizer')
    speakers = models.ManyToManyField(User, verbose_name='palestrantes', related_name='speaker')
    tags = models.ManyToManyField(Tag, verbose_name='tags')
    description = models.TextField(verbose_name='descrição')
    ticket_price = models.FloatField(verbose_name='preço do ingresso')
    start_dt = models.DateTimeField('início')
    end_dt = models.DateTimeField('fim')

    def __str__(self):
        return f'{self.name} by {self.organizer}'
    
    def get_duration(self):
        return self.end_dt - self.start_dt

    def get_ticket_price_display(self):
        if self.ticket_price:
            return self.ticket_price
        else:
            return 'Evento gratuito!'
