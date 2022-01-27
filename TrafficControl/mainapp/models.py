from django.db import models
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
