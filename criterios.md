# Criterios

* desde 6 horas antes del amanecer hasta 2 horas despues, viento de tierra->mar (mayoría del tiempo)
* desde 2 horas después del amanecer hasta 2 horas después del atardecer, 2 horas continuas de viento mar->tierra
* desde 2 horas después del atardecer hasta 6 después del atardecer, viento tierra->mar (mayoría del tiempo)

amanecer  = x
atardecer = y

|------------------|----------------------|-------------------------|
|-----------------------|----------------------|--------------------|
|         !D            |          D           |          !D        |
+-----------------------+----------------------+--------------------+

# Detectar D
if hora_actual >= amanecer+2 and hora_actual < atardecer+2:
	# estamos en D
else:
	# estamos en !D
