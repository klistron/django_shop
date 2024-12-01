from django.db import models

class Payment(models.Model):
    "Класс для работы с платежами"
    number = models.CharField(max_length=16, verbose_name="Номер карты")
    name = models.CharField(max_length=100, verbose_name="Имя владельца карты")
    month = models.CharField(max_length=2, verbose_name="Месяц на карте")
    year = models.CharField(max_length=4, verbose_name="Год на карте")
    code = models.CharField(max_length=3, verbose_name="CVV")
