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

	datos_hoy  = []
	dia_actual = {
		'noD': 0,
		'tierramar': 0,
		'martierra': 0,
		'C2': False,
	}

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

		if angulo != -999.90:
			# Detectar si es de día
			if hora_actual >= amanecer+dos and hora_actual < atardecer+dos:
				# es de día
				if not dia_actual['C2']:
					if es_mar_tierra(normal, amplitud, angulo):
						dia_actual['martierra'] += 1

						if dia_actual['martierra'] >= 12:
							dia_actual['C2'] = True
					else:
						dia_actual['martierra'] = 0
			else:
				# madrugada y noche
				dia_actual['noD'] += 1
				if es_tierra_mar(normal, amplitud, angulo):
					dia_actual['tierramar'] += 1

		if hora == 23 and minuto == 50:
			# final del día, revisamos si hubo brisa hoy

			mensaje = 'no'
			if dia_actual['noD'] > 0 and dia_actual['tierramar']/dia_actual['noD'] > .6 and dia_actual['C2']:
				mensaje = 'SI<---'

			print(anio, mes+1, dia+1, mensaje, sep='\t')

			dia_actual = {
				'noD': 0,
				'tierramar': 0,
				'martierra': 0,
				'C2': False,
			}
