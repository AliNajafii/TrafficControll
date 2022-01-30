from django.shortcuts import render
from rest_framework import viewsets
from .models import Owner,Car
from .serializers import OwnerModelSerializer,CarModelSerializer

class OwnerAPIViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerModelSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args,**kwargs)

class CarAPIViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args,**kwargs)
