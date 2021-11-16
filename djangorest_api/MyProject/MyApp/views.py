from .models import Lekarz,Pacjent
from rest_framework import viewsets
from .serializers import LekarzSerializer,PacjentSerializer

class LekarzViewSet(viewsets.ModelViewSet):
    queryset = Lekarz.objects.all()
    serializer_class = LekarzSerializer

class PacjentViewSet(viewsets.ModelViewSet):
    queryset = Pacjent.objects.all()
    serializer_class = PacjentSerializer