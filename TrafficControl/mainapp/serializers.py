from rest_framework import serializers
from .models import Owner,Car,CarTraffic,CarTypes,ColorTypes
from django.db.models import ObjectDoesNotExist
import logging
logg = logging.Logger(__name__,level=logging.DEBUG)
class DynamicFieldsSerializer(serializers.ModelSerializer):
    """
    With this class we can specify our fiels
    when serializer initialized.
    """
    def __init__(self,*args,**kwargs):
        fields = kwargs.pop('fields',None)

        super().__init__(*args,**kwargs)

        if fields:
            #filtering fields by droping it
            allowed = set(fields)
            existing = set(self.fields.keys())
            for f_name in existing - allowed:
                #removing unwanted fields
                self.fields.pop(f_name)

class BulkOwnerCreate(serializers.ListSerializer):

    def create(self,validated_date):
        """
        this create method is for creating
        one owner instance.
        """
        owners = []
        cars = []
        for data in validated_date:
            cars_data = None
            try:
                cars_data = data.pop('ownerCar')
            except KeyError:
                pass
            owner = Owner(**data)
            owners.append(owner)
            if cars_data:
                for car_data in cars_data:
                    color = ColorTypes.get_type(car_data.pop('color'))
                    car_type = CarTypes.get_type(car_data.pop('car_type'))
                    
                    car = Car(
                    owner = owner,
                    car_type=car_type,
                    color=color
                    ,**car_data)

                    cars.append(car)

        owners = Owner.objects.bulk_create(owners)
        Car.objects.bulk_create(cars)
        return owners


class CarModelSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Car
        fields = (
            'id',
            'owner',
            'car_type',
            'load_valume',
            'color',
            )
        read_only_fields = ['owner',]
    
    def create(self,validated_data):
        car_type = CarTypes.get_type(validated_data.pop('car_types')) 
        car_color = ColorTypes.get_type(validated_data.pop('color'))
        owner_id = validated_data.pop('owner')
        try:
            owner = Owner.objects.get(id=owner_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
            'owner does not exists.please create owner first'
        )
        return Car.objects.create(
            owner=owner,
            car_type = car_type,
            color = car_color
            )

class OwnerModelSerializer(DynamicFieldsSerializer):
    ownerCar = CarModelSerializer(many=True,required=False)
    class Meta:
        model = Owner
        fields = (
            'name',
            'age',
            'total_toll_paid',
            'ownerCar'
        )
        list_serializer_class = BulkOwnerCreate
    
    def create(self,validated_date):
        """
        this create method is for creating
        one owner instance.
        """
        cars_data = None
        cars = []
        try:
            cars_data = validated_date.pop('ownerCar')
     
        except KeyError:
            pass
        owner = Owner.objects.create(**validated_date)
        if cars_data:
            for car_data in cars_data:
                color = ColorTypes.get_type(car_data.pop('color'))
                car_type = CarTypes.get_type(car_data.pop('car_type'))
                cars.append(Car(
                    owner = owner,
                    car_type=car_type,
                    color=color,**car_data
                    ))
            Car.objects.bulk_create(cars)
        return owner
    
class BulkCreateCarTrafficSerializer(serializers.ListSerializer):
    """
    associates with CarTraffic serializer to create 
    bulk data.
    """
    def create(self,validated_date):
        cars_trrafics = [
            CarTraffic(**data) for data in validated_date
        ] #Traffics of cars

        return CarTraffic.objects.bulk_create(cars_trrafics)


class CarTrafficModelSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Car
        fields = ('car','date','lat','lng')
        list_serializer_class = BulkCreateCarTrafficSerializer
    
