from .models import Doctor,Patient,Visit,Specialization
from rest_framework import viewsets
from .serializers import DoctorSerializer,PatientSerializer,VisitSerializer,HospitalUserSerializer,SpecializationSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    authentication_classes = []
    serializer_class = DoctorSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    authentication_classes=[]
    serializer_class = PatientSerializer

class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    authentication_classes = []
    serializer_class = SpecializationSerializer

class VisitViewSet(viewsets.ViewSet):
    queryset = Visit.objects.all()
    authentication_classes = []
    serializer_class = VisitSerializer

    def get_queryset(self):
        specialization_id=self.request.query_params.get('specialization_id')
        return Visit.objects.filter(doctor__specialization_id=specialization_id).distinct()