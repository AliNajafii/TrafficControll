from django.test import TestCase
from .models import Owner,Car
from .models import CarTypes,ColorTypes
from django.db.utils import OperationalError
from .utils import LimitedQueryMixin
from geo.models import Road

class OwnerModelTest(TestCase):
    """
        Note:
        beacuse django test uses different
        DB the designed Trigger in main DB
        for checking the big car constraint
        of each owner is ignored.
        But i tested it in shell and it worked.
        """ 
    def setUp(self):
        Owner.objects.all().delete()
        Car.objects.all().delete()
        self.owner1 = Owner(
            name = 'o1',
            age = 50,
            national_code = 182764533,
            total_toll_paid = None
        )
        self.owner1.save()

        super().setUp()
    
    def test_adding_many_small_cars_to_owner(self):
        self.owner2 = Owner.objects.create(
            id = 7,
            name = 'Ali',
            age = 23,

        )
        car3 = Car.objects.create(
            car_type = CarTypes.SMALL.value,
            load_balance = None,
            color = ColorTypes.RED.value,
            owner = self.owner2
        )
        car4 = Car.objects.create(
            car_type = CarTypes.SMALL.value,
            load_balance = 200,
            color = ColorTypes.BLUE.value,
            owner = self.owner2
        )
        car5 = Car.objects.create(
            car_type = CarTypes.SMALL.value,
            load_balance = 100,
            color = ColorTypes.GREEN.value,
            owner = self.owner2
        )

        self.assertEqual(self.owner2.car_set.all().count(),3)
        self.assertIn(car3,self.owner2.car_set.all())

class TestLimitQueryMixin(TestCase):
    
    def setUp(self):
        for i in range(1,101):
            Road.objects.create(name=f'r{i}',width=f'{i}')
    
    def test_limit_query_count(self):
        all_roads = Road.objects.all()
        #with percent of .2 it should send 20 items 
        count = len(list(next(Road.limit_query(all_roads))))
        self.assertEqual(count,20)

        all_roads = Road.objects.all()
        count = len(list(next(Road.limit_query(all_roads,percent=.5))))
        self.assertEqual(count,50)

    def test_limit_query_item(self):
        r1 = Road.objects.get(name='r1')
        all_roads = Road.objects.all()
        some_roads = Road.limit_query(all_roads)
        self.assertIn(r1,next(some_roads))

        all_roads = Road.objects.all()
        r35 = Road.objects.get(name='r35')
        some_roads = Road.limit_query(all_roads,offset=34)

        self.assertIn(r35,next(some_roads))
        
        
        
        
        

        

