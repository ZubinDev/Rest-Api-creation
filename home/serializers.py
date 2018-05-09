from rest_framework import serializers
from home.models import Circuit, Customer, Site


class FileSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'customer_name', 'city', 'state', 'address')


class CircuitSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Circuit
        fields = ('id', 'customer','circuit_id', 'mep_id', 'cir_az', 'cir_za')


class SiteSerializer(serializers.ModelSerializer):
    circuit = CircuitSerializer()

    class Meta:
        model = Site
        fields = ('id', 'circuit', 'ip', 'hw_version','type')




