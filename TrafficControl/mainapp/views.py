from django.shortcuts import render
from rest_framework import viewsets
from .models import Owner,Car
from .serializers import OwnerModelSerializer,CarModelSerializer

class OwnerAPIViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerModelSerializer

class CarAPIViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
