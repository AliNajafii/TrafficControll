from django.test import TestCase
from .models import Road,Route,TollStation
import random as rand

#---models first stage testing
class RouteModelToolsMixin :
    """a Mixin class to help Testcase to produce 
    Route test instances
    """
    def random_coordinates(self,float_number=6):
        """
        returns random latitude and longitude
        """
        lat = rand.randrange(-90,90)
        lat_float = str(rand.random())[:float_number+2]
        lat += float(lat_float)

        lng = rand.randrange(-180,180)
        lnt_float = str(rand.random())[:float_number+2]
        lnt += float(lnt_float)

        return lat,lnt

    def make_random_routes(self,road:Road,number:int=4):
        """
        makes random Rout objects for
        the given road object.
        """
        for _ in range(number):
            lat,lng = self.random_coordinates()
            Route.objects.create(
                lat = lat,
                lng = lng,
                road = road
            )
       



