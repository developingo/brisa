#!/usr/bin/env python3
import csv
import json
import sys
import os
from pytz import timezone
from datetime import datetime, timedelta

def dd(alpha, beta):
    return (beta - alpha)%360

def es_tierra_mar(normal, amplitud, angulo):
    return dd(normal, angulo) <= amplitud/2 or dd(angulo, normal) <= amplitud/2

def es_mar_tierra(normal, amplitud, angulo):
    return es_tierra_mar((normal+180)%360, amplitud, angulo)

meses = [
    'enero',
    'febrero',
    'marzo',
    'abril',
    'mayo',
    'junio',
    'julio',
    'agosto',
    'septiembre',
    'octubre',
    'noviembre',
    'diciembre',
]

if __name__ == '__main__':
    if len(sys.argv)==1:
        print("Falta la estacion!")
        exit(1)

    estacion = sys.argv[1]

    try:
        archivo_datos = open('%s/%s.csv'%(estacion, estacion))
        archivo_angulos = open('%s/angle.txt'%estacion)
        archivo_coords = open('%s/coords.txt'%estacion)
    except FileNotFoundError as error:
        print("No existe el archivo %s"%error.filename)
        exit()

    normal = float(archivo_angulos.readline())
    amplitud = float(archivo_angulos.readline())
    estacion_lon = float(archivo_coords.readline())

    result_csv = csv.writer(open('%s/result.csv'%estacion, 'w'))

    citla_csv = csv.reader(archivo_datos)

    veracruz_lon = -96.15333333333334
    offset_hour = (veracruz_lon - estacion_lon)/360*24
    offset_min = int(offset_hour*60)
    offset_sec = int((offset_hour*60 - offset_min)*60)

    offset = timedelta(minutes=offset_min, seconds=offset_sec)

    dos = timedelta(hours=2)
    tz  = timezone('America/Mexico_City')

    sunrise_data = json.load(open('sunrise_utc.json'))

    print("Calculos iniciales terminados...")
    print("Procesando datos...")

    datos_hoy  = []
    dia_actual = {
        'noD': 0,
        'tierramar': 0,
        'martierra': 0,
        'C2': False,
    }

    if not os.path.isdir('%s/meses'%estacion):
        os.mkdir('%s/meses'%estacion)

    meses_csv = [
        csv.writer(open('%s/meses/%02d_%s.csv'%(estacion, mes, meses[mes-1]), 'w'))
        for mes in range(1, 13)
    ]

    for fila in citla_csv:
        anio   = int(fila[0])
        mes    = int(fila[1])
        dia    = int(fila[2])
        hora   = int(fila[3])
        minuto = int(fila[4])

        angulo     = float(fila[5])
        intensidad = float(fila[7])

        hora_actual = datetime(anio, mes, dia, hora, minuto, 0, tzinfo=tz)

        fecha = '%d-%d-%d'%(anio, mes, dia)
        amanecer  = datetime.strptime(sunrise_data[fecha]['sunrise'], '%Y-%m-%d %H:%M:%S%z') + offset
        atardecer = datetime.strptime(sunrise_data[fecha]['sunset'], '%Y-%m-%d %H:%M:%S%z') + offset

        if angulo != -999.90:
            datos_hoy.append([
                anio, mes, dia, hora, minuto, angulo, intensidad
            ])
            # Detectar si es de día
            if hora_actual >= amanecer+dos and hora_actual < atardecer+dos:
                # es de día
                if not dia_actual['C2']:
                    if es_mar_tierra(normal, amplitud, angulo):
                        dia_actual['martierra'] += 1

                        if dia_actual['martierra'] >= 12:
                            dia_actual['C2'] = True
                    else:
                        dia_actual['martierra'] = 0
            else:
                # madrugada y noche
                dia_actual['noD'] += 1
                if es_tierra_mar(normal, amplitud, angulo):
                    dia_actual['tierramar'] += 1

        if dia == 1 and hora == 0 and minuto == 0:
            # Inicio del mes

            print(mes, end='')

        if hora == 23 and minuto == 50:
            # final del día, revisamos si hubo brisa hoy
            print('.', end='')
            sys.stdout.flush()

            mensaje = 0
            if dia_actual['noD'] > 0 and dia_actual['tierramar']/dia_actual['noD'] > .6 and dia_actual['C2']:
                mensaje = 1

                meses_csv[mes - 1].writerows(datos_hoy)

            datos_hoy = []

            result_csv.writerow([anio, mes, dia, mensaje])

            dia_actual = {
                'noD': 0,
                'tierramar': 0,
                'martierra': 0,
                'C2': False,
            }

    print()
