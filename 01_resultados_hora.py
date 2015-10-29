# -*- coding:utf-8 -*-
# Calculo del promedio por hora
from math import sin, cos, sqrt, atan, pi
import sys

if __name__ == '__main__':
	if len(sys.argv)==1:
		print("Falta la estacion!")
		exit(1)

	estacion = sys.argv[1]

	# Archivo de entrada
	archivo          = open('%s/%s.txt'%(estacion,estacion))

	# Archivos de resultados
	archivo_res_comp = open('%s/01_resultados_hora_comp.txt'%(estacion), 'w')
	archivo_res      = open('%s/01_resultados_hora.txt'%(estacion), 'w')

	hora_actual = '0'
	u_list      = []
	v_list      = []
	fecha       = []

	for linea in archivo:
		data        = list(filter(lambda x:x, linea.strip().split(' ')))

		if int(data[3]) > 8:
			continue

		intensidad  = data[7]
		direccion   = data[5]
		minutos     = data[4]

		if not fecha:
			fecha = data[:3]

		u = -1 * float(data[7]) * sin(pi/180*float(data[5]))
		v = -1 * float(data[7]) * cos(pi/180*float(data[5]))

		if data[3] == hora_actual:
			if data[7] != '-999.90':
				u_list.append(u)
				v_list.append(v)
		else:
			if len(u_list) >= 3:
				# Si hay tres o más valores se calculan los promedios para escribir
				# en los archivos
				promedio_u = sum(u_list)/len(u_list)
				promedio_v = sum(v_list)/len(v_list)

				if promedio_v != 0:
					direccion_prom  = 180/pi*atan(promedio_u/promedio_v)
					intensidad_prom = sqrt(promedio_u**2 + promedio_v**2)
				else:
					intensidad_prom = 0
					direccion_prom  = 0

				# Archivo con las componentes promedio
				archivo_res_comp.write('\t'.join(fecha + [hora_actual] + [str(promedio_u), str(promedio_v)]) + '\n')
				# Archivo con los promedios por hora
				archivo_res.write('\t'.join(fecha + [hora_actual] + [str(direccion_prom), str(intensidad_prom)]) + '\n')
			else:
				# Si no hay suficientes valores entonces es hora de escribir algunos NaN
				archivo_res_comp.write('\t'.join(fecha + [hora_actual] + ['NaN', 'NaN']) + '\n')
				archivo_res.write('\t'.join(fecha + [hora_actual] + ['NaN', 'NaN']) + '\n')

			if data[3] == '0':
				fecha = []

			hora_actual = data[3]

			u_list = []
			v_list = []

			if data[7] != '-999.90':
				u_list.append(u)
				v_list.append(v)
