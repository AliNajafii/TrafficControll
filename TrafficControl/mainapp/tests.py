from django.test import TestCase
from .models import Owner,Car
from .models import CarTypes,ColorTypes
from django.db.utils import OperationalError
from django.db.models import QuerySet
from django.utils.timezone import datetime
from geo.models import Road
from threading import Lock
lock = Lock()

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
            load_valume = None,
            color = ColorTypes.RED.value,
            owner = self.owner2
        )
        car4 = Car.objects.create(
            car_type = CarTypes.SMALL.value,
            load_valume = 200,
            color = ColorTypes.BLUE.value,
            owner = self.owner2
        )
        car5 = Car.objects.create(
            car_type = CarTypes.SMALL.value,
            load_valume = 100,
            color = ColorTypes.GREEN.value,
            owner = self.owner2
        )

        self.assertEqual(self.owner2.car_set.all().count(),3)
        self.assertIn(car3,self.owner2.car_set.all())


        
    
    


        

