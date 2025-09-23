
import os

import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'API.settings')

print('DJANGO_SETTINGS_MODULE' in os.environ)

django.setup()


import pandas as pd

condf = pd.read_csv("./data/test_consumos_10_users.csv")
gendf = pd.read_csv("./data/generacion.csv")

conlist = list (condf.itertuples(index=False, name=None))

genlist = list (gendf.itertuples(index=False, name=None))


print(conlist[0][0], conlist[0][1], conlist[0][2])

consumos = []

for c in conlist:
    consumos.append((c[0],c[2],c[1])) 


with connection.cursor() as cursor:
    cursor.executemany("INSERT INTO apiv2_generación (timestamp, generacion) VALUES (?, ?)", genlist)
    cursor.executemany("INSERT INTO apiv2_consumo (uid, consumo, timestamp) VALUES (?, ?, ?)", consumos)