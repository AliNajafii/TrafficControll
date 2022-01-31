from .models import Road,Route,TollStation
from rest_framework import serializers 
from django.db.models import ObjectDoesNotExist


#---Model Serializers
class RouteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('lat','lng',)

class BulkRoadCreate(serializers.ListSerializer):
    
    """
    this serializer is for bulk creation.
    client can pass Road route point too.
    """
    def create(self,validated_data):
        roads=[]
        routes_data = None
        for data in validated_data:
            try:
                routes_data = data.pop('route_set')
            except KeyError:
                pass
            road = Road.objects.create(**data)
            roads.append(road)
            if routes_data:
                for r_data in routes_data:
                    Route.objects.create(road=road,**r_data)
        
        
        return roads

class RoadModelSerializer(serializers.ModelSerializer):
    """
    Serializes The Road objects
    """
    route_set = RouteModelSerializer(many=True,required=False,label='points')
    class Meta :
        model = Road
        fields = ('name','width','route_set',)
        list_serializer_class = BulkRoadCreate
    
    def create(self,validated_data):
        
        points = validated_data.pop('route_set')
        
        road = Road.objects.create(**validated_data)
        for point_data in points :
            Route.objects.create(road=road,**point_data)
        return road
    
    def update(self,instance,validated_data):
        routes_data = None
        try :
            routes_data = validated_data.pop('route_set')
        except KeyError:
            pass
        try:
            road = Road.objects.get(id=instance.id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
        f'Road {instance.name} , {instance.width} does not exists.'
        )
        

class BulkTollStationSerializer(serializers.ListSerializer):
    """
    this serializer is for creating bulk toll station
    """
    def create(self,validated_data):
        stations = [TollStation(**data) for data in validated_data]
        return TollStation.objects.bulk_create(stations) 

class TollStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TollStation
        exclude = ('id',)
        list_serializer_class = BulkTollStationSerializer
    
    