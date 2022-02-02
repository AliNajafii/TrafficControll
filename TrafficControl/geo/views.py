from django.shortcuts import render
from.models import Road,TollStation
from .sreializers import(
    RoadModelSerializer,
    TollStationSerializer,
    PositionSerializer
)

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class RoadAPIViewSet(viewsets.ModelViewSet):
    queryset = Road.objects.all()
    serializer_class = RoadModelSerializer
    lookup_field = 'name'

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args,**kwargs)
    
    @action(
        methods=['get'],
        detail=False,name='roads with tollStations',
        url_path='with-tollstations'
        )
    def roads_with_tollStation(self,request,*args,**kwargs):
        """
        returns all roads which have tollsations on them
        """
        objects = Road.roads_with_toll_station()
        seri = self.serializer_class(objects,many=True)
        return Response(seri.data)

class TollStationAPIViewSet(viewsets.ModelViewSet):
    queryset = TollStation.objects.all()
    serializer_class = TollStationSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args,**kwargs)
    
    @action(
        methods=['post'],
        detail=True,
        name='position near toll station',
        url_path = 'position-near'
        )
    def is_position_near(self,request,pk=None):
        """
        this action is acting like TollStation model
        class 'is_position_near' method.
        client should specify exact tollStaion
        there for this action is in detail.
        client should just send it's lat and long
        and radius range in km .
        system returns True or false.
        """
        seri = PositionSerializer(data=request.data)
        seri.is_valid(raise_exception=True)
        lat = seri.data['lat']
        lng = seri.data['lng']
        r = seri.data['radius']
        ts = TollStation.objects.get(pk=pk)
        result = ts.is_position_near(lat,lng,r)
        return Response(
            {
                'result':result
            }
        )

