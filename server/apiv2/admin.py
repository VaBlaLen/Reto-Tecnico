from django.contrib import admin
from .models import Consumo, Generación

# Register your models here.

admin.site.register(Consumo)
admin.site.register(Generación)