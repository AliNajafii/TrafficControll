from .models import Road,Route,TollStation
from rest_framework import serializers 


#---Model Serializers
class RouteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class RoadModelSerializer(serializers.ModelSerializer):
    """
    Serializes The Road objects
    """
    points = RouteModelSerializer(many=True)
    class Meta :
        model = Road
        fields = ('name','width','points',)
    
    def create(self,validated_data):
        points = validated_data.pop('points')
        road = Road.objects.create(**validated_data)
        for point_data in points :
            Route.objects.create(road=road,**point_data)
        return road

class TollStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TollStation
        exclude = ('id',)