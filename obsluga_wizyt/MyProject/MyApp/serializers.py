from rest_framework import serializers
from .models import Specialization,Doctor,Patient,Visit,HospitalUser

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields=['name']

class HospitalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalUser
        fields=['first_name','last_name','date_of_birth','username','password','objects','USERNAME_FIELD']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields=['specialization']



class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields=['doctor','date','location']