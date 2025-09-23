from rest_framework import serializers
from apiv2.models import Consumo, Generación

class ConsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumo
        fields = ["uid", 'consumo', 'timestamp']

class GeneracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generación
        fields = ['timestamp','generacion']

class GenlistSerializer(serializers.ModelSerializer):
    results = GeneracionSerializer(many=True)
    class Meta:
        model = Generación
        fields = ['results']

class ConlistSerializer(serializers.ModelSerializer):
    results = ConsumoSerializer(many=True)
    class Meta:
        model = Consumo
        fields = ['results']