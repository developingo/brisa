import sys

def err(*args):
    print(*args, file=sys.stderr)

def obten_estacion():
    if len(sys.argv) == 1:
        estacion = 'btordo'
    else:
        estacion = sys.argv[1]

    if estacion.endswith('/'):
        estacion = estacion[:-1]

    err('Usando la estacion %s'%estacion)

    return estacion

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

estaciones = {
    'btordo'    : 'Barra de tordo',
    'citla'     : 'Citlaltepec',
    'cang'      : 'Cangrejera',
    'sfernando' : 'San Fernando',
    'rio'       : 'Río lagartos',
    'paraiso'   : 'Paraíso',
    'dzim'      : 'Dzilam',
    'celestm'   : 'Celestun',
    'cdcarmn'   : 'Ciudad del Carmen',
    'campe'     : 'Campeche',
}

angles = [i*45 for i in range(8)]

if __name__ == '__main__':
    obten_estacion()
