#!/usr/bin/env python3
# Calcula la normal a la playa
import matplotlib.pyplot as plt
import numpy as np
from math import atan, acos, pi, sin, cos
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import sys

action   = 'coast'
coast_x  = []
coast_y  = []
stat_x   = 0
stat_y   = 0
xlim     = 0
ax       = None
estacion = ''

def do_compute():
    x_data = np.array(coast_x)
    y_data = np.array(coast_y)

    x_mean = sum(x_data)/len(x_data)
    y_mean = sum(y_data)/len(y_data)

    c_factor = x_data - x_mean

    m1 = sum(y_data * c_factor) / sum(x_data * c_factor)
    b1 = y_mean - x_mean * m1

    # best fit plot
    f = lambda x: m1*x + b1

    bf_x = np.linspace(0, xlim, 50)
    bf_y = f(bf_x)

    plt.plot(bf_x, bf_y, 'g-')

    # ortogonal line plot
    m2 = -1/m1
    b2 = stat_x/m1 + stat_y
    g = lambda x: m2*x + b2

    ort_x = np.linspace(0, xlim, 50)
    ort_y = g(ort_x)

    plt.plot(ort_x, ort_y, 'g-')

    # Intersection
    int_x = (b2 - b1)/(m1 - m2)
    int_y = m2*int_x + b2
    plt.plot(int_x, int_y, 'bo')

    # Direction vector
    theta = atan(m1)
    d_x, d_y = cos(theta), sin(theta)

    magic = 500

    left_x = int_x + magic*d_x
    left_y = int_y + magic*d_y

    right_x = int_x - magic*d_x
    right_y = int_y - magic*d_y

    a_vec = np.array([left_x - stat_x, left_y - stat_y])
    b_vec = np.array([right_x - stat_x, right_y - stat_y])

    aperture = 180/pi*acos(np.dot(a_vec, b_vec)/(np.linalg.norm(a_vec)*np.linalg.norm(b_vec)))

    degree = 90 + 180/pi*atan(-1/m1)

    plt.title('Angulo tierra a mar: %.4f\nApertura: %.4f'%(degree, aperture))
    with open('%s/angle.txt'%estacion, 'w') as infofile:
        infofile.writelines([
            "%.6f\n"%degree,
            "%.6f\n"%aperture,
        ])

    path = mpath.Path([
        (stat_x, stat_y),
        (left_x, left_y),
        (right_x, right_y),
        (None, None),
    ], [
        mpath.Path.MOVETO,
        mpath.Path.LINETO,
        mpath.Path.LINETO,
        mpath.Path.CLOSEPOLY,
    ])

    patch = mpatches.PathPatch(path, facecolor='r', alpha=0.5)

    ax.add_patch(patch)

    plt.draw()

def onpick(event):
        global action
        global coast
        global stat_x
        global stat_y

        x = event.xdata
        y = event.ydata

        if event.button == 3:
            if action == 'coast':
                action = 'station'
                plt.title("Escoge la ubicacion de la estacion")
                plt.draw()
                return
            else:
                exit()

        if action == 'coast':
            coast_x.append(x)
            coast_y.append(y)
            plt.plot(x, y, 'ro')
        elif action == 'station':
            plt.plot(x, y, 'bo')
            stat_x = x
            stat_y = y
            do_compute()
            action = 'exit'
        else:
            pass
        plt.draw()

if __name__ == '__main__':
    if len(sys.argv)==1:
        print("Falta la estacion!")
        exit(1)
    
    estacion = sys.argv[1]

    fig, ax = plt.subplots()

    image = plt.imread('%s/%s.jpg'%(estacion, estacion))

    ax.imshow(image)
    ax.autoscale(False)

    xlim = ax.get_xlim()[1]

    cid = fig.canvas.mpl_connect('button_press_event', onpick)

    plt.title("Escoge los puntos de la costa")
    plt.xlabel("Click derecho cuando termines ;)")

    plt.show()
