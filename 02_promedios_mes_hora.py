#!/usr/bin/env python3
# -*- coding:utf8 -*-
# Calculo del promedio por hora
from math import sin, cos, sqrt, atan, pi
import sys
if __name__ == '__main__':
	if len(sys.argv)==1:
		print "Falta la estacion!"
		exit(1)

	estacion = sys.argv[1]

	archivo_comp = open('%s/01_resultados_hora_comp.txt'%(estacion), 'r')
	resultados   = open('%s/02_promedios_mes_hora.txt'%(estacion), 'w')
	# año	mes	dia	hora	comp_u	comp_v

	meses = [[{'u':[], 'v':[]} for i in range(9)] for i in range(12)]

	for linea in archivo_comp:
		data = linea.strip().split('\t')

		anio = int(data[0])
		mes  = int(data[1])
		dia  = int(data[2])
		hora = int(data[3])

		valor_u = float(data[4])
		valor_v = float(data[5])

		if data[4] != 'NaN':
			meses[mes-1][hora]['u'].append(valor_u)
			meses[mes-1][hora]['v'].append(valor_v)

	for num_mes, mes in enumerate(meses):
		for num_hora, hora in enumerate(mes):
			if len(hora['u']) >= 3:
				prom_u = sum(hora['u'])/len(hora['u'])
				prom_v = sum(hora['v'])/len(hora['v'])

				direccion_prom  = 180/pi*atan(prom_u/prom_v)
				intensidad_prom = sqrt(prom_u**2 + prom_v**2)

				resultados.write('\t'.join(map(str, [num_mes+1, num_hora, intensidad_prom, direccion_prom])) + '\n')
			else:
				resultados.write('\t'.join(map(str, [num_mes+1, num_hora, 'NaN', 'NaN'])) + '\n')

