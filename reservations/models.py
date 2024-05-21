from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    event_date = models.DateField(verbose_name='Data do Evento')
    reservation_date = models.DateField(auto_now_add=True, verbose_name='Data de Reserva')
    
    def __str__(self):
        return f'Reserva por {self.user.username}'
