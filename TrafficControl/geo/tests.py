from django.test import TestCase
from .models import Road,Route,TollStation
import random as rand

class TestRoad(TestCase):
    """
    testing Road functionalities
    """

    def setUp(self):
        r1 = Road.objects.create(name='r1',width='22.87567')
        r2 = Road.objects.create(name='r2',width='6.22')
        r3 = Road.objects.create(name='r3',width='8.70')

        Route.objects.create(lat='0',lng='0',road=r1)
        Route.objects.create(lat='1',lng='1',road=r1)
        Route.objects.create(lat='2',lng='0',road=r1)
        Route.objects.create(lat='1',lng='3',road=r1)
        Route.objects.create(lat='2',lng='4',road=r1)

        Route.objects.create(lat='0',lng='0',road=r2)
        Route.objects.create(lat='2',lng='2',road=r2)
        Route.objects.create(lat='3',lng='4',road=r2)
        Route.objects.create(lat='3',lng='5',road=r2)
        Route.objects.create(lat='3',lng='6',road=r2)

        Route.objects.create(lat='3',lng='6',road=r3)
        Route.objects.create(lat='4',lng='5',road=r3)
        Route.objects.create(lat='5',lng='4',road=r3)
        Route.objects.create(lat='6',lng='4',road=r3)
        Route.objects.create(lat='7',lng='4',road=r3)

        TollStation.objects.create(
            name='T1',
            lat='3',
            lng='4.5',
            toll_per_cross = 300
            )#placed in r2
        TollStation.objects.create(
            name='T2',
            lat='5.874',
            lng='4',
            toll_per_cross = 200
            )#placed in r3
        TollStation.objects.create(
            name='T3',
            lat='12.2',
            lng='14.98',
            toll_per_cross = 100
            )#placed in none of them
    
    def test_in_this_road(self):
        r1 = Road.objects.get(name='r1')
        t1 = TollStation.objects.get(name='T1')
        in_r1 = r1.in_this_road(*t1.get_position())

        self.assertEqual(in_r1,False)

        r2 = Road.objects.get(name='r2')
        in_r2 = r2.in_this_road(*t1.get_position())

        self.assertEqual(in_r2,True)

        roads_with_toll_station = Road.roads_with_toll_station()
        r3 = Road.objects.get(name='r3')
        self.assertIn(r2,roads_with_toll_station)
        self.assertIn(r3,roads_with_toll_station)
        
    
    


       



