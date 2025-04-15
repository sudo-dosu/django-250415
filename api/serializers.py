from rest_framework import serializers
from .models import City, IDC, Host


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class IDCSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDC
        fields = '__all__'


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'
