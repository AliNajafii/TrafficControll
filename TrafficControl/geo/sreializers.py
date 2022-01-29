from .models import Road,Route,TollStation
from rest_framework import serializers 


#---Model Serializers
class RouteModelSerializer(serializers.ModelSerializer)

class RoadModelSerializer(serializers.ModelSerializer):
    """
    Serializes The Road objects
    """
    routs = serializers.HyperlinkedModelSerializer()
    class Meta :
        model = Road
        fields = ('name')