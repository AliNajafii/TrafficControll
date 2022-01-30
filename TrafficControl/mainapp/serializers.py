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
        fields = '__all__'

class CarModelSerializer(DynamicFieldsSerializer):

    class Meta:
        model = Car
        fields = '__all__'

class CarTrafficModelSerializer(DynamicFieldsSerializer):

    class Meta:
        model = Car
        fields = '__all__'
