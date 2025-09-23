from django.db import models

# Create your models here.
class Consumo(models.Model):
    uid = models.IntegerField(blank=False, null=False)
    consumo = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(blank=False, null=False)
    class Meta:
        ordering = ['uid', 'timestamp']

class Generación(models.Model):
    timestamp = models.DateTimeField(blank=False, null=False)
    generacion = models.FloatField(default=0.0)

    class Meta:
        ordering = ['timestamp']
