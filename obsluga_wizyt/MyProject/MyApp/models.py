from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models

class Specialization(models.Model):
    name = models.CharField(max_length=30)

class HospitalUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    username=models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()
    USERNAME_FIELD = 'username'

class Doctor(HospitalUser):
    specialization = models.ManyToManyField(Specialization)

class Patient(HospitalUser):
    pass

class Visit(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    date = models.DateField()
    location = models.CharField(max_length=30)