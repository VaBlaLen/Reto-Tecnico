from rest_framework import serializers
from apiv1.models import Consumo, Generación

class ConsumoSerializer(serializers.ModelSerializer):
    uid = serializers.IntegerField(source='id')
    class Meta:
        model = Consumo
        fields = ["uid", 'consumo', 'timestamp']

class GeneracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generación
        fields = '__all__'