from django.shortcuts import render
from.models import Road,TollStation
from .sreializers import RoadModelSerializer,TollStationSerializer
from rest_framework import viewsets

class RoadAPIViewSet(viewsets.ModelViewSet):
    queryset = Road.objects.all()
    serializer_class = RoadModelSerializer
    lookup_field = 'name'

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args,**kwargs)

class TollStationAPIViewSet(viewsets.ModelViewSet):
    queryset = TollStation.objects.all()
    serializer_class = TollStationSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args,**kwargs)
