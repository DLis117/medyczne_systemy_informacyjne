from rest_framework import serializers
from .models import Specjalizacja,Lekarz,Pacjent,Visit,HospitalUser

class LekarzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lekarz
        fields=['specjalizacja']

class SpecjalizacjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specjalizacja
        fields=['nazwa']

class HospitalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalUser
        fields=['first_name','last_name','date_of_birth','username','password','objects','USERNAME_FIELD']


class PacjentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacjent
        fields=['id','imie','nazwisko','oddzial','data_urodzenia']


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields=['doctor','date','location']