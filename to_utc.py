#!/usr/bin/env python3
import csv
from datetime import datetime
from pytz import timezone
import json

archivo_amanecer = open('sunrise_sunset.csv', 'r')

amanecer_csv = csv.reader(archivo_amanecer)

tz  = timezone('America/Mexico_City')
utc = timezone('UTC')

utc_data = {}

for fila in amanecer_csv:
    hora_amanecer = datetime(
        int(fila[0]),
        int(fila[1]),
        int(fila[2]),
        *map(int, fila[3].split(':')),
        tzinfo=tz
    )
    atardecer = list(map(int, fila[4].split(':')))
    hora_atardecer = datetime(
        int(fila[0]),
        int(fila[1]),
        int(fila[2]),
        atardecer[0]+12,
        atardecer[1],
        tzinfo=tz
    )

    utc_data[fila[0] + '-' + fila[1] + '-' + fila[2]] = {
        'sunrise': hora_amanecer.astimezone(utc).strftime('%Y-%m-%d %H:%M:%S%z'),
        'sunset': hora_atardecer.astimezone(utc).strftime('%Y-%m-%d %H:%M:%S%z'),
    }

json.dump(utc_data, open('sunrise_utc.json', 'w'))
