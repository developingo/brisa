#!/usr/bin/env python3
from matplotlib import pyplot as plt
from math import pi
from numpy import arange
import sys
import csv
import os

# Etiquetas empiezan aquí ↓ Terminan aqui ↓
rad_grid        = arange(.5,               3, .5)
#                  Y avanzan en saltos de esto ↑

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Falta el archivo')
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print('No existe el archivo en la ruta %s'%sys.argv[1])
        exit(1)

    csv_reader = csv.reader(open(sys.argv[1]))

    theta = []
    radii = []
    for line in csv_reader:
        theta.append(float(line[0])*pi/180 + pi)
        radii.append(float(line[1]))

    ax   = plt.subplot(111, projection='polar')

    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rgrids(rad_grid)
    ax.autoscale(False)

    bars = ax.plot(theta, radii, 'o-')

    # labels
    for index, (θ, r) in enumerate(zip(theta, radii)):
        plt.text(θ, r, index+1)

    plt.show()
