from rest_framework import serializers
from .models import Lekarz,Pacjent
class LekarzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lekarz
        fields=['id','imie','nazwisko','oddzial','profesja']



class PacjentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacjent
        fields=['id','imie','nazwisko','oddzial','data_urodzenia']