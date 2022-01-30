from django.db import models
from .utils import make_line,in_line,in_radius_range
from django.db.models import QuerySet
from mainapp.utils import LimitedQueryMixin 


class Position(models.Model):
    """
    This class represents the position
    wich have latitude and longitude.
    to avoiding violation of Single Responsibility
    I seprated the 'position' meaning to three
    independent meanings:
    1- position as a constant for places
    2- set of positions as Route
    3 - combination of position and time :
    represents the movement.
    """
    lat = models.CharField(max_length=25)
    lng = models.CharField(max_length=25)
    

    class Meta:
        abstract = True

class AbstractBaseRoad(models.Model):
    """roads features
    This class has all features
    of a road. like name and width
    """
    name = models.CharField(max_length=30,null=True,blank=True)
    width = models.CharField(max_length=15)
    class Meta:
        abstract = True

class Road(AbstractBaseRoad,LimitedQueryMixin):
    """
    Each road has many routs
    """

    class Meta:
        unique_together = ['name','width']
    

    @classmethod
    def roads_with_toll_station(cls):
        """
        returns all roads  which have
        toll stations in them.
        """
        all_toll_stations = TollStation.objects.all()
        toll_stations_without_specified_road = set()
        response_roads = set()
        for t in all_toll_stations:
            if not t.road :
                toll_stations_without_specified_road.add(t)
            else :
                road = cls.objects.get(road=t.road)
                response_roads.add(road)

            for toll in all_toll_stations :
                if toll not in toll_stations_without_specified_road:
                    all_roads = cls.objects.all()
                    if not all_roads:
                        return response_roads 
                    for road in all_roads.iterator(): #for better performance using limit
                        if road.in_this_road(t.lat,t.lng):
                            response_roads.add(road)
                            t.road = road
                            t.save()
        return response_roads
            
    
    def in_this_road(self,lat,lng):
        """
        returns True if a point is
        in this road.
        """
        points = self.route_set.all().values_list('lat','lng')
        line = make_line(*points)
        return in_line(lat,lng,line)
    
    
class Route(Position):
    """Represents a path position
    Route it self represents a single position
    of a whole Path.
    """
    road = models.ForeignKey(
        'Road',
        on_delete=models.PROTECT,
        )

class TollStation(Position):
    """Represents Toll stations
    Tollstation is a place then it 
    has a position.
    """
    name = models.CharField(max_length=10)
    toll_per_cross = models.IntegerField()
    per_kilogram_cost = models.IntegerField(default=300)
    road = models.ForeignKey(
        'Road',
        on_delete = models.CASCADE,
        null = True,
        blank = True
    ) #this field at first is null based on our 
        #data set but for searching faster
        #when querying to find a tollstation is located
        # in which road , we can inisialize this field
    
    def get_position(self):
        
        return self.lat , self.lng
    
    def is_position_near(self,
        lat:float,
        lng:float,
        in_radius:float):
        """
        returns True if a position
        is in the radius range of this toll
        station.
        """
        center = self.get_position()
        return in_radius_range(*center,lat,lng,in_radius)
    
    
