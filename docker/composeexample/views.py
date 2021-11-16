from django.shortcuts import render
from .models import Idea
from rest_framework import viewsets
from .serializers import IdeaSerializer
class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer