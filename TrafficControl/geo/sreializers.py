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
    routes = RouteModelSerializer(many=True,label='path-points')
    class Meta :
        model = Road
        fields = ('name','width','routs')

class TollStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TollStation
        exclude = ('id',)