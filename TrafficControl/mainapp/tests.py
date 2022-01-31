from django.test import TestCase
from .models import Owner,Car
from .models import CarTypes,ColorTypes
from django.db.utils import OperationalError
from django.db.models import QuerySet
from django.utils.timezone import datetime
from geo.models import Road
from .mixins import CarInfoDataExtractorMixin,InfoDataExtractorMixin

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
    
class TestCarTypes(TestCase):

    def test_get_type(self):
        small = CarTypes.get_type('small')
        big = CarTypes.get_type('big')
        self.assertEqual(small,'SM')
        self.assertEqual(big,'BG')

        small = CarTypes.get_type('SmaLl')
        big = CarTypes.get_type('BiG')

        self.assertEqual(small,'SM')
        self.assertEqual(big,'BG')

class TestColorTypes(TestCase):

    def test_get_type(self):
        red = ColorTypes.get_type('red')
        blue = ColorTypes.get_type('blue')
        black = ColorTypes.get_type('black')
        white = ColorTypes.get_type('white')

        self.assertEqual(red,'RD')
        self.assertEqual(blue,'BL')
        self.assertEqual(black,'BK')
        self.assertEqual(white,'WH')

        red = ColorTypes.get_type('Red')
        blue = ColorTypes.get_type('blUe')
        black = ColorTypes.get_type('bLacK')
        white = ColorTypes.get_type('WhitE')

        self.assertEqual(red,'RD')
        self.assertEqual(blue,'BL')
        self.assertEqual(black,'BK')
        self.assertEqual(white,'WH')


class InfoExtractor(TestCase):

    def setUp(self):
            self.data = {
            "name": "Mohammad",
            "national_code": 8569875425,
            "age": 72,
            "total_toll_paid": 2000,
            "ownerCar": [
                {
                    "id": 3,
                    "car_type": "small",
                    "color": "White",
                    "length": 3.1,
                    "load_valume": None
                },
                {
                    "id": 4,
                    "car_type": "big",
                    "color": "red",
                    "length": 6.3,
                    "load_valume": 125.0
                }
            ]
        }
    
    def test_info_extract(self):
        extractor = InfoDataExtractorMixin()
        extractor.valid_names = ['ownerCar','car_set']
        data = extractor.extract_info(self.data)
        self.assertIsInstance(data,list)
        print(data)
        for d in data:
            self.assertIsNotNone(d.get('id'))
            self.assertIsNotNone(d.get('car_type'))
            self.assertIsNotNone(d.get('color'))
            self.assertIsNotNone(d.get('length'))
            self.assertIsNotNone(d.get('load_valume'))
    
    def test_car_info_extract(self):
        extractor = CarInfoDataExtractorMixin()
        data = extractor.extract_info(self.data)
        self.assertIsInstance(data,list)
        for d in data:
            self.assertIsNotNone(d.get('id'))
            self.assertIsNotNone(d.get('car_type'))
            self.assertIsNotNone(d.get('color'))
            self.assertIsNotNone(d.get('length'))
            self.assertIsNotNone(d.get('load_valume'))

    
    


        

