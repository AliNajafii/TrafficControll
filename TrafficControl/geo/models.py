from django.db import models

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
    name = models.CharField(max_length=30)
    width = models.CharField(max_length=15)
    class Meta:
        abstract = True

class Road(AbstractBaseRoad):
    """
    Each road has many routs
    """

    class Meta:
        unique_together = ['name','width']
    
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
    Tollstation is a place the it 
    has a position.
    """
    name = models.CharField(max_length=10)
    toll_per_cross = models.IntegerField()

    
    
