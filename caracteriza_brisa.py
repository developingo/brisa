#!/usr/bin/env python3
"""
Toma los concentrados de cada mes y calcula un día promedio de brisa de ese mes
en la carpeta prom
"""
import sys
import csv
import os
from math import sin, cos, pi, atan, sqrt
from util import obten_estacion, err, meses

if __name__ == '__main__':
    estacion = obten_estacion()

    if not os.path.isdir('%s/meses'%estacion):
        os.mkdir('%s/meses'%estacion)

    if not os.path.isdir('%s/prom'%estacion):
        os.mkdir('%s/prom'%estacion)

    for indice, mes in enumerate(meses):
        try:
            mes_csv  = csv.reader(open('%s/meses/%02d_%s.csv'%(estacion, indice+1, mes)))
            prom_csv = csv.writer(open('%s/prom/%02d_%s.csv'%(estacion, indice+1, mes), 'w'))
        except FileNotFoundError as e:
            err('No existe el archivo %s'%e.filename)
            err('Quizá olvidaste ejecutar antes detecta_brisa.py')
            exit(1)

        horas = [
            {
                'u': 0,
                'v': 0,
                'n': 0,
            } for i in range(24)
        ]

        for fila in mes_csv:
            direccion  = float(fila[5])
            intensidad = float(fila[6])

            hora = int(fila[3])

            if intensidad != -999.9:
                u = -1 * float(intensidad) * sin(pi/180*float(direccion))
                v = -1 * float(intensidad) * cos(pi/180*float(direccion))

                horas[hora]['u'] += u
                horas[hora]['v'] += v
                horas[hora]['n'] += 1

        for hora, data in enumerate(horas):
            if data['n'] > 0:
                promedio_u = data['u'] / data['n']
                promedio_v = data['v'] / data['n']

                direccion_prom  = (180/pi*atan(promedio_u/promedio_v))%360
                intensidad_prom = sqrt(promedio_u**2 + promedio_v**2)
            else:
                direccion_prom  = 0
                intensidad_prom = 0

            prom_csv.writerow([direccion_prom,intensidad_prom])
