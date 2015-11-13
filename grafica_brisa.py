#!/usr/bin/env python3
from math import pi
import matplotlib.pyplot as plt
import csv
import sys

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

angles = [i*45 for i in range(8)]

labels = [i*3 for i in range(8)]

rlabel = [(i+1)*2 for i in range(6)]

if __name__ == '__main__':
    if len(sys.argv)==1:
        print("Falta la estacion!")
        exit(1)

    estacion = sys.argv[1]

    fig, axes = plt.subplots(2, 6)

    for indice, mes in enumerate(meses):
        prom_csv = csv.reader(open('%s/prom/%02d_%s.csv'%(estacion, indice+1, mes)))

        radius = []

        ax = plt.subplot(2, 6, indice+1, projection='polar')

        for row in prom_csv:
            radius.append(float(row[1]))

        theta = [i/24*2*pi for i in range(24)] + [0]
        radius += radius[:1]

        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_thetagrids(angles, labels)
        ax.set_rgrids(rlabel, rlabel)
        ax.autoscale(False)

        for i, r in enumerate(radius):
            ax.arrow(i/24*2*pi, r, 0, 1)

        ax.plot(theta, radius)
        ax.set_title(mes)

    plt.suptitle(estacion)

    plt.show()
