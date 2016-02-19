#!/usr/bin/env python3
# Calculo del promedio por hora de todos los datos
from math import sin, cos, sqrt, atan, pi
from util import obten_estacion

if __name__ == '__main__':
	estacion = obten_estacion()

	archivo          = open('%s/%s.csv'%(estacion, estacion))
	archivo_res_comp = open('%s/prom_comp.csv'%estacion, 'w')
	archivo_res      = open('%s/prom.csv'%estacion, 'w')

	hora_actual = '0'
	u_list      = []
	v_list      = []
	fecha       = []

	for linea in archivo:
		data        = list(filter(lambda x:x, linea.strip().split(',')))
		intensidad  = data[7]
		direccion   = data[5]
		if not fecha:
			fecha = data[:3]

		u = -1 * float(intensidad) * sin(pi/180*float(direccion))
		v = -1 * float(intensidad) * cos(pi/180*float(direccion))

		if data[3] == hora_actual:
			if intensidad != 'NaN':
				u_list.append(u)
				v_list.append(v)
		else:
			if len(u_list) >= 3:
				# Si hay tres o más valores se calculan los promedios para escribir
				# en los archivos
				promedio_u = sum(u_list)/len(u_list)
				promedio_v = sum(v_list)/len(v_list)

				direccion_prom  = 180/pi*atan(promedio_u/promedio_v)
				intensidad_prom = sqrt(promedio_u**2 + promedio_v**2)

				# Archivo con las componentes promedio
				archivo_res_comp.write('\t'.join(fecha + [hora_actual] + [str(promedio_u), str(promedio_v)]) + '\n')
				# Archivo con los promedios por hora
				archivo_res.write('\t'.join(fecha + [hora_actual] + [str(direccion_prom%360), str(intensidad_prom)]) + '\n')
			else:
				# Si no hay suficientes valores entonces es hora de escribir algunos NaNs
				archivo_res_comp.write('\t'.join(data[:3] + [hora_actual] + ['NaN', 'NaN']) + '\n')
				archivo_res.write('\t'.join(data[:3] + [hora_actual] + ['NaN', 'NaN']) + '\n')

			if data[3] == '0':
				fecha = []

			hora_actual = data[3]

			u_list = []
			v_list = []

			if intensidad != 'NaN':
				u_list.append(u)
				v_list.append(v)
