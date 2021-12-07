from .models import Lekarz,Pacjent,Specjalizacja,Visit
from rest_framework import viewsets
from .serializers import LekarzSerializer,PacjentSerializer,HospitalUserSerializer,VisitSerializer,SpecializacjaSerializer


class LekarzViewSet(viewsets.ModelViewSet):
    queryset = Lekarz.objects.all()
    authentication_classes = []
    serializer_class = LekarzSerializer

class PacjentViewSet(viewsets.ModelViewSet):
    queryset = Pacjent.objects.all()
    authentication_classes = []
    serializer_class = PacjentSerializer

class SpecjalizacjaViewSet(viewsets.ModelViewSet):
    queryset = Specjalizacja.objects.all()
    authentication_classes = []
    serializer_class = SpecializacjaSerializer

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    authentication_classes = []
    serializer_class = VisitSerializer

    def get_queryset(self):
        specialization_id = self.request.query_params.get('specialization_id')
        return Visit.objects.filter(doctor__specialization_id=specialization_id).distinct()
