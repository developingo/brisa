#!/usr/bin/env python3
"""
Toma los días promedio calculados por caracteriza_brisa.py y los grafica en
coordenadas polares.
"""
from math import pi, sqrt, cos, sin, asin
from util import obten_estacion, err, estaciones, meses, angles
import matplotlib.pyplot as plt
import csv
import sys

labels = [i*3 for i in range(8)]

rlabel = [(i+1)*2 for i in range(6)]

theta = [i/24*2*pi for i in range(24)] + [0]

if __name__ == '__main__':
    estacion = obten_estacion()

    for indice, mes in enumerate(meses):
        try:
            prom_csv = csv.reader(open('%s/prom/%02d_%s.csv'%(estacion, indice+1, mes)))
        except FileNotFoundError as e:
            err('No existe el archivo %s'%e.filename)
            err('Quizá olvidaste ejecutar caracteriza_brisa.py')
            exit(1)

        radius = []
        gammas = []

        ax = plt.subplot(2, 6, indice+1, projection='polar')

        for row in prom_csv:
            radius.append(float(row[1]))
            gammas.append(float(row[0]) / 360 * 2 * pi)

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
        ax.set_title(mes)

    plt.suptitle(estaciones[estacion])

    plt.show()
