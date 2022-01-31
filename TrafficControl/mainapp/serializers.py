from rest_framework import serializers
from .models import Owner,Car,CarTraffic,CarTypes,ColorTypes
from django.db.models import ObjectDoesNotExist
from .mixins import CarInfoDataExtractorMixin
from django.db import transaction

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


class CarModelSerializer(DynamicFieldsSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Car
        fields = (
            'id',
            'owner',
            'car_type',
            'load_valume',
            'length',
            'color',
            )
        read_only_fields = ['owner',]
    
    def create(self,validated_data):
        
        owner_id = validated_data.pop('owner')
        try:
            owner = Owner.objects.get(id=owner_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
            'owner does not exists.please create owner first'
        )
        return Car.objects.create(
            owner=owner,
            **validated_data
            )

class BulkOwnerCreate(
    serializers.ListSerializer,
    CarInfoDataExtractorMixin
    ):
    
    def create(self,validated_date):
        """
        this create method is for creating
        one owner instance.
        """
       
        owners = []
        
        for data in validated_date:
                cars_data = self.extract_info(data)
                owner = Owner(**data)
                owner.save()
                owners.append(owner)
                if cars_data:
                    for car_data in cars_data:
                        car = Car.objects.create(owner=owner,**car_data)
                        
        return owners


class OwnerModelSerializer(
    DynamicFieldsSerializer,
    CarInfoDataExtractorMixin
    ):
    ownerCar = CarModelSerializer(many=True,required=False)
    class Meta:
        model = Owner
        fields = (
            'name',
            'national_code',
            'age',
            'total_toll_paid',
            'ownerCar',
        )
        list_serializer_class = BulkOwnerCreate
    
    
    def create(self,validated_date):
        """
        this create method is for creating
        one owner instance.
        """
        print(validated_date)
        cars_data = self.extract_info(validated_date)
        cars = []
        owner = Owner.objects.create(**validated_date)
        if cars_data:
            for car_data in cars_data:
                car = Car.objects.create(owner=owner,**car_data)
        
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
        fields = ('car','date','lat','lng',)
        list_serializer_class = BulkCreateCarTrafficSerializer
    
