from rest_framework import routers
from .views import LekarzViewSet,PacjentViewSet
from django.urls import include,path
router= routers.DefaultRouter()
router.register(r'lekarze',LekarzViewSet)
router.register(r'pacjenci',PacjentViewSet)


urlpatterns=[path('',include(router.urls)),
             path('api-auth/',include('rest_framework.urls',namespace='rest_framework'))
]