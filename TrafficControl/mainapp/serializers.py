from rest_framework import serializers
from .models import Owner,Car,CarTraffic

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


class OwnerModelSerializer(DynamicFieldsSerializer):
    
    class Meta:
        model = Owner
        fields = (
            'name',
            'age',
            'total_toll_paid',
        )
    

class CarModelSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Car
        fields = (
            'owner',
            'car_type',
            'load',
            'load_balance',
            'color',
            )

class OwnerWithCarSerializer(OwnerModelSerializer):
    ownerCar = CarModelSerializer(many=True)
    class Meta:
        fields = OwnerModelSerializer.Meta.fields + ('cars',)
    
    def create(self,validated_date):
        cars = {}
        try:
            cars = validated_date.pop('ownerCar')
        except KeyError:
            pass
        owner = Owner.objects.create(**validated_date)
        for car_data in cars :
            Car.objects.create(owner=owner,**car_data)

class CarTrafficModelSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Car
        fields = ('car','date','lat','lng')
