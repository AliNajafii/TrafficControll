from django.shortcuts import render
from.models import Road,TollStation
from .sreializers import RoadModelSerializer
from rest_framework import viewsets

class RoadAPIViewSet(viewsets.ModelViewSet):
    queryset = Road.objects.all()
    serializer_class = RoadModelSerializer
