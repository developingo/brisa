#!/usr/bin/env python3
import csv
import json
import sys
from pytz import timezone
from datetime import datetime, timedelta

def dd(alpha, beta):
	return (beta - alpha)%360

def es_tierra_mar(normal, amplitud, angulo):
	return dd(normal, angulo) <= amplitud/2 or dd(angulo, normal) <= amplitud/2

def es_mar_tierra(normal, amplitud, angulo):
	return es_tierra_mar((normal+180)%360, amplitud, angulo)

if __name__ == '__main__':
	if len(sys.argv)==1:
		print("Falta la estacion!")
		exit(1)

	estacion = sys.argv[1]

	try:
		archivo_datos = open('%s/%s.csv'%(estacion, estacion))
		archivo_angulos = open('%s/angle.txt'%estacion)
		archivo_coords = open('%s/coords.txt'%estacion)
	except FileNotFoundError as error:
		print("No existe el archivo %s"%error.filename)
		exit()

	normal = float(archivo_angulos.readline())
	amplitud = float(archivo_angulos.readline())
	estacion_lon = float(archivo_coords.readline())

	anios = {
		2008: [[] for m in range(0, 12)],
		2009: [[] for m in range(0, 12)],
		2010: [[] for m in range(0, 12)],
		2011: [[] for m in range(0, 12)],
		2012: [[] for m in range(0, 12)],
	}

	citla_csv = csv.reader(archivo_datos)

	veracruz_lon = -96.15333333333334
	offset_hour = (veracruz_lon - estacion_lon)/360*24
	offset_min = int(offset_hour*60)
	offset_sec = int((offset_hour*60 - offset_min)*60)

	offset = timedelta(minutes=offset_min, seconds=offset_sec)

	dos = timedelta(hours=2)
	tz  = timezone('America/Mexico_City')

	sunrise_data = json.load(open('sunrise_utc.json'))

	print("Calculos iniciales terminados...")
	print("Procesando datos...")
	anio_actual = ''

	for fila in citla_csv:
		anio   = int(fila[0])
		mes    = int(fila[1]) - 1
		dia    = int(fila[2]) - 1
		hora   = int(fila[3])
		minuto = int(fila[4])

		angulo     = float(fila[5])

		hora_actual = datetime(anio, mes+1, dia+1, hora, minuto, 0, tzinfo=tz)

		fecha = '%d-%d-%d'%(anio, mes+1, dia+1)
		amanecer  = datetime.strptime(sunrise_data[fecha]['sunrise'], '%Y-%m-%d %H:%M:%S%z') + offset
		atardecer = datetime.strptime(sunrise_data[fecha]['sunset'], '%Y-%m-%d %H:%M:%S%z') + offset

		if anio_actual != anio:
			anio_actual = anio
			print()
			print(anio_actual)

		if hora == 0 and minuto == 0:
			print('.', end='')
			sys.stdout.flush()
			anios[anio][mes].append({
				'noD': 0,
				'tierramar': 0,
				'martierra': 0,
				'C2': False,
			})

		if angulo == -999.90:
			continue

		# Detectar si es de día
		if hora_actual >= amanecer+dos and hora_actual < atardecer+dos:
			# es de día
			if not anios[anio][mes][dia]['C2']:
				if es_mar_tierra(normal, amplitud, angulo):
					anios[anio][mes][dia]['martierra'] += 1

					if anios[anio][mes][dia]['martierra'] >= 12:
						anios[anio][mes][dia]['C2'] = True
				else:
					anios[anio][mes][dia]['martierra'] = 0
		else:
			# madrugada y noche
			anios[anio][mes][dia]['noD'] += 1
			if es_tierra_mar(normal, amplitud, angulo):
				anios[anio][mes][dia]['tierramar'] += 1

	for anio in range(2008, 2013):
		for num_mes, mes in enumerate(anios[anio]):
			for num_dia, dia in enumerate(mes):
				mensaje = 'no'
				if dia['noD'] > 0 and dia['tierramar']/dia['noD'] > .6 and dia['C2']:
					mensaje = 'SI<---'

				print(anio, num_mes+1, num_dia+1, mensaje, sep='\t')
