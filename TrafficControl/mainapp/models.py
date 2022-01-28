from django.db import models
from django.db.models import Q
from geo.models import Position
from enum import Enum

class ColorTypes(Enum):
    RED = 'RD'
    BLUE = 'BL'
    YELLOW = 'YL'
    GREEN = 'GR'

class CarTypes(Enum):
    SMALL = 'sml'
    BIG = 'big'

class Person(models.Model):
    """
    Person is an abstract concept
    for all other persons in system.
    """
    name = models.CharField(
        max_length= 15
    )
    age = models.IntegerField()
    national_code = models.CharField(
        max_length= 12
    )

    class Meta:
        abstract = True

class Owner(Person):
    """A Person who has cars
    Each Owner could have many
    smal(light) car and only one
    heavy car.
    """
    total_toll_paid = models.IntegerField(
        null=True,
        blank=True
        )
    
    @classmethod
    def violated_owners(cls):
        """
        returns all owners which didnt
        pay their Toll but passed from
        them.
        violated owners are passed the tollstations
        but did not paied. it means total_toll_paid
        is null or from when they tracked we excpect
        that total_toll_paid will be more than the amount
        we expected.
        """
    
    
    
    
class Car(models.Model):
    """Represents Car
    A class which has 
    features of a car.
    note : an owner can't have more than one
    heavy car.therefore i will create
    a mysql Trigger to handel this constraint.
    """
    car_type = models.CharField(
        max_length = 3,
        choices= (
            (CarTypes.SMALL.value,CarTypes.SMALL.name),
            (CarTypes.BIG.value,CarTypes.BIG.name),
        )
         
    )
    
    load_balance = models.IntegerField(
        null= True,
        blank= True
    )
    COLOR_CHOICES = (
        (ColorTypes.BLUE.value,ColorTypes.BLUE.name),
        (ColorTypes.RED.value,ColorTypes.RED.name),
        (ColorTypes.GREEN.value,ColorTypes.GREEN.name),
    )
    color = models.CharField(
        max_length=2,
        choices= COLOR_CHOICES
    )
    owner = models.ForeignKey(
        'Owner',
        on_delete = models.CASCADE,
        related_query_name= 'cars'
    )

    def path_traveled(self,start_date=None,end_date=None):
        """
        return positions traveld by this car
        betwwen start_date and end_date
        """
        if (start_date and not end_date) or (end_date and not start) :
            raise ValueError('you should set both start_date and end_date')

        if not start_date and not end_date:
            return self.cartraffic_set.all().values_list('lat','lng')
            
        between_date = Q(date__range=(start_date,end_date))
        points = self.cartraffic_set.all().filter(between_date).values_list('lat','lng')
        return list(points)


class CarTraffic(Position):
    """represants traffic of spesific car
    Car Traffic is designed to show car
    movements and tracked coordinates.
    """
    car = models.ForeignKey(
        'Car',
        on_delete = models.CASCADE,
        related_query_name= 'movements'
    )

    date = models.DateTimeField()
