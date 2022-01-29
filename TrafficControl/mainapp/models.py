from django.db import models
from django.db.models import Q
from geo.models import Position
from enum import Enum
from geo import utils as geoutils
from geo.models import TollStation
from .utils import LimitedQueryMixin

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
    
    def path_traveled(self):
        """
        return list of pathes travelled
        by owner cars.
        """
        points_list = []
        for car in self.car_set.all():
            points = car.path_traveled()
            points_list.append(points)
        return points_list
    
    def path_traveld_by_car(self,car_id):
        """
        return the path which travelled by
        her/him car.
        """
        try:
            car = self.car_set.get(pk=car_id)
        except models.ObjectDoesNotExist:
            return 
        return car.path_traveled()
    
    def toll_stations_passed_by_specific_car(self,car_id):
        """
        returns all toll stations that owner passed
        by a specific car.
        """
        toll_stations = []
        positions = self.path_traveld_by_car(car_id)
        if positions:
            travelled_path = geoutils.make_line(*positions)
            for ts in TollStation.objects.all():
                lat,lng = ts.get_position()
                if geoutils.in_line(lat,lng,travelled_path):
                    toll_stations.append(ts)
        return toll_stations
        


    
    def toll_station_passed(self,cartype = CarTypes.BIG):
        """
        returns total toll stations passed
        by owner cars. default car type is 
        just big cars.
        """
        toll_stations = []
        for car in self.car_set.all():
            toll_stations += self.toll_stations_passed_by_specific_car(car.id)
        
        return toll_stations


    def expected_total_toll_price_for_small_cars(self):
        """
        returns amount of total toll
        prices which system expects
        from owner when driving small 
        cars and should to pay.
        """
        total_price = 0
        total_toll_stations = \
            self.toll_station_passed(CarTypes.SMALL) #when driving with small car
                                                    #and passing from toll stations
        
        for ts in total_toll_stations:
            total_price += ts.toll_per_cross
        
        return total_price
    
    def expected_total_toll_price_for_big_cars(self):
        """
        returns total pay amount
        when owner driving big car
        and pass the toll station
        it should pay per load balance.
        """
        total_price = 0
        try:
            big_car = self.car_set.filter(car_type = CarTypes.BIG)[0]
            toll_stations_passed = self.toll_stations_passed_by_specific_car(big_car.id)
            for ts in toll_stations_passed:
                price = big_car.load_balance * ts.per_kilogram_cost
                total_price += price
        except IndexError:
            pass

        return total_price
    
    def expected_total_toll_price(self):
        """
        return total price that system
        expects owner should paid.
        """
        return self.expected_total_toll_price_for_big_cars() \
            + self.expected_total_toll_price_for_small_cars()
    
    
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
    
    def get_position(self,
        in_date_time=None,
        start_date=None,
        end_date=None
        ):
        """
        get the position of the car by
        given datetime.
        it returns car traffic instances
        """
        this_car_traffics = Q(car__id = self.id)
        if in_date_time:
            date = Q(date=in_date_time)
            try:
                car_traffic = CarTraffic.objects.filter(this_car_traffics and date)
                return car_traffic
            except IndexError:
                return CarTraffic.objects.none()

        elif start_date and end_date :
            date = Q(date__range=(start_date,end_date))
            this_car_traffics = CarTraffic.objects.filter(this_car_traffics and date).order_by('-date')
            return this_car_traffics
            


class CarTraffic(Position,LimitedQueryMixin):
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

    @classmethod
    def get_list_of_car_position_by_date(cls,
        car_type = CarTypes.BIG,
        in_date_time=None,
        start_date=None,
        end_date=None
        ):
        """
        returns list of cars positions
        at given date time .
        """
        car_query = Q(car__car_type = car_type.value)
        if in_date_time :
            date = Q(date=date)
            cars_position = CarTraffic.objects.filter(date and car_query)
            return cars_position
        elif start_date and end_date :
            date = Q(date__range=(start_date,end_date))
            cars_position = CarTraffic.objects.filter(date and car_type)
            return cars_position
        else :
            raise ValueError('in_date_time or start_date and end_date should be given')




    
