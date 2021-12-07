from django.contrib import admin
from .models import Doctor
from .models import Patient
admin.site.register(Doctor)
admin.site.register(Patient)
# Register your models here.
