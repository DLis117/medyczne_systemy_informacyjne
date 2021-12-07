from rest_framework import routers
from .views import DoctorViewSet,PatientViewSet,VisitViewSet,SpecializationViewSet
from django.urls import include,path
router= routers.DefaultRouter()
router.register(r'doctors',DoctorViewSet)
router.register(r'patients',PatientViewSet)
router.register(r'specializations',SpecializationViewSet)
router.register(r'visits',VisitViewSet)



urlpatterns=[path('',include(router.urls)),
             path('api-auth/',include('rest_framework.urls',namespace='rest_framework'))
]