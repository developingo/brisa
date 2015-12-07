#!/usr/bin/env python3
"""
Calcula el día promedio de brisa en esta estación, usando los datos de cada mes
luego lo grafica
"""
import sys
import csv
import os
from math import sin, cos, pi, atan, sqrt, asin
from util import obten_estacion, err, estaciones, angles, meses
import matplotlib.pyplot as plt

labels = [i*3 for i in range(8)]

rlabel = [(i+1)*2 for i in range(6)]

theta = [i/24*2*pi for i in range(24)] + [0]

if __name__ == '__main__':
    estacion = obten_estacion()

    if not os.path.isdir('%s/prom'%estacion):
        os.mkdir('%s/prom'%estacion)

    prom_csv = csv.writer(open('%s/prom/promedio.csv'%estacion, 'w'))

    horas = [
        {
            'u': 0,
            'v': 0,
            'n': 0,
        } for i in range(24)
    ]

    for indice, mes in enumerate(meses):
        try:
            mes_csv  = csv.reader(open('%s/meses/%02d_%s.csv'%(estacion, indice+1, mes)))
        except FileNotFoundError as e:
            err('No existe el archivo %s'%e.filename)
            err('Quizá olvidaste ejecutar antes detecta_brisa.py')
            exit(1)

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

    radius = []
    gammas = []

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

        radius.append(intensidad_prom)
        gammas.append(direccion_prom / 360 * 2 * pi)

    err('Done computing! lets plot!')

    ax = plt.subplot(projection='polar')

    radius += radius[:1]

    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_thetagrids(angles, labels)
    ax.set_rgrids(rlabel, rlabel)
    ax.autoscale(False)

    for i, (γ, r) in enumerate(zip(gammas, radius)):
        θ = i/24*2*pi
        β = pi - γ + θ
        c = sqrt(r**2 + 1 - 2*r*cos(β))
        Δr = c - r
        Δθ = asin(sin(β)/c)
        ax.arrow(θ, r, Δθ, Δr, head_width=.05, head_length=.04)

    ax.plot(theta, radius)

    plt.suptitle(estaciones[estacion])

    plt.show()
