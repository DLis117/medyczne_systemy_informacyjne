from django.db import models

class Lekarz(models.Model):
    imie=models.CharField(max_length=100)
    nazwisko=models.CharField(max_length=100)
    oddzial=models.CharField(max_length=100)
    profesja = models.CharField(max_length=100)
    def __str__(self):
        return self.imie

class Pacjent(models.Model):
    imie=models.CharField(max_length=100)
    nazwisko=models.CharField(max_length=100)
    oddzial=models.CharField(max_length=100)
    data_urodzenia=models.DateField()
    def __str__(self):
        return self.imie