#!/usr/bin/env python3
import sys
import csv
import os
from math import sin, cos, pi, atan, sqrt

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

    if not os.path.isdir('%s/meses'%estacion):
        os.mkdir('%s/meses'%estacion)

    if not os.path.isdir('%s/prom'%estacion):
        os.mkdir('%s/prom'%estacion)

    for indice, mes in enumerate(meses):
        mes_csv  = csv.reader(open('%s/meses/%02d_%s.csv'%(estacion, indice+1, mes)))
        prom_csv = csv.writer(open('%s/prom/%02d_%s.csv'%(estacion, indice+1, mes), 'w'))

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
            promedio_u = data['u'] / data['n']
            promedio_v = data['v'] / data['n']

            direccion_prom  = (180/pi*atan(promedio_u/promedio_v))%360
            intensidad_prom = sqrt(promedio_u**2 + promedio_v**2)

            prom_csv.writerow([direccion_prom,intensidad_prom])
