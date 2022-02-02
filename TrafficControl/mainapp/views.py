from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Owner,Car,CarTraffic,CarTypes,ColorTypes
from django.utils import timezone
from geo.models import TollStation
from .serializers import (
    OwnerModelSerializer,
    CarModelSerializer,
    CarTrafficModelSerializer
)
from rest_framework.exceptions import ValidationError
from datetime import datetime
from TrafficControl.settings import TRAFFIC_DATA_DATE_FORMATE

class OwnerAPIViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerModelSerializer
    lookup_field = 'national_code'

    def get_serializer(self, *args, **kwargs):
        """
        If list of json data received
        it makes serializer to act as
        a list serializer.
        """
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args,**kwargs)
    
    def delete(self,*args,**kwargs):
        dls = self.queryset.delete()
        return Response(dls)
    
    @action(
        methods=['get'],
        detail=False,
        name = 'violated owners list',
        url_path = 'violated-list'
    )
    def violated_owners(self,request):
        """
        returns all violated owners
        """
        violated = Owner.violated_owners()
        seri = self.get_serializer_class()(violated,many=True)
        return Response(seri.data)

class CarAPIViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args,**kwargs)

    
    def get_queryset(self):
        """
        to handeling url parameters
        and filter by url params
        """
        query = self.queryset  
        color = self.request.query_params.get('color')
        owner_age_less_than = self.request.query_params.get('age__lte')
        owner_age_more_than = self.request.query_params.get('age__gt')
        print(self.request.query_params)
        if color:
            if ',' in color:
                colors = color.split(',')
                for c in colors:
                    index = colors.index(c)
                    color = ColorTypes.get_type(c)
                    colors[index] = color
                query = query.filter(color__in=colors)
            else :
                color = ColorTypes.get_type(color)
                if color:
                    query = query.filter(color=color)
        if owner_age_less_than:
            if owner_age_less_than.isnumeric():
                query = query.filter(owner__age__lte = owner_age_less_than)
        if owner_age_more_than:
            if owner_age_more_than.isnumeric():
                query = query.filter(owner__age__gt = owner_age_more_than)
        
        return query
    
    @action(
        methods=['post'],
        detail=False,
        name='cars in range of a tollStation',
        url_path = 'cars-near-tollStation'
        )
    def cars_near_tollStation(self,request):
        """
        returns all cars that are near
        a toll station by range in specified date.
        client should send toll station
        name and date.
        """
        print(self.request.query_params)
        print('-------------------------')
        toll_name = request.data.get('toll_name')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        radius = request.data.get('radius')
        
        if not all([start_date,end_date,radius,toll_name]):
            raise ValidationError('toll_name,start_date,end_date and radius are required')
        
        radius = float(radius)
        
        start_date = datetime.strptime(start_date,TRAFFIC_DATA_DATE_FORMATE)
        end_date = datetime.strptime(end_date,TRAFFIC_DATA_DATE_FORMATE)
        cars= []
        all_cars = self.get_queryset()
        toll_station = TollStation.objects.get(name=toll_name)
        for car in all_cars:
            points = car.path_traveled(start_date,end_date)
            for lat,lng in points:
                if toll_station.is_position_near(lat,lng,radius):
                    cars.append(car)
        
        seri = self.get_serializer_class()(cars,many=True)
        return Response(seri.data)
    
    @action(
        methods=['post'],
        detail = False,
        name='cars passed unaouthorized roads',
        url_path = 'cars-passage'
    )
    def cars_passages(self,request):
        """
        returns cars with the given type
        which passed from roads with the width of
        less than given amount.
        client should send
        """
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        car_type = request.data.get('car_type')
        road_width = request.data.get('road_width')
        if not all([start_date,end_date,road_width]):
            raise ValidationError(
            {
                'Error':'start_date,end_date and road_width is required.'
            }
            )
        start_date = datetime.strptime(start_date,TRAFFIC_DATA_DATE_FORMATE)
        end_date = datetime.strptime(end_date,TRAFFIC_DATA_DATE_FORMATE)
        road_width = float(road_width)
        cars = []
        if car_type:
            car_type = CarTypes.get_type(car_type)
            if car_type:
                cars = Car.cars_passed(
                    road_width,
                    start_date,
                    end_date,
                    car_type
                    )
        else :
            cars = Car.cars_passed(road_width,start_date,end_date)
        
        seri = self.get_serializer_class()(cars,many=True)
        return Response(seri.data)
    
    @cars_passages.mapping.options
    def keys(self,request):
        """
        returns wich keys client should
        send to /cars-passge/ url.
        """
        return Response({
            "road_width":['required','float'],
            "car_type":['not reqiured','string'],
            "start_date":['not required','string'],
            "end_date":['not required','string'], 
        })

class CarTrafficAPIViewSet(viewsets.ModelViewSet):
    queryset = CarTraffic.objects.all().order_by('-date')
    serializer_class = CarTrafficModelSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args,**kwargs)
