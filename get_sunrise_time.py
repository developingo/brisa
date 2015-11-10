from pyquery.pyquery import PyQuery
from itertools import starmap
import csv

def get_hour(hour_text):
    return hour_text.split(' ')[0]

def get_row(year, month, index, row, res):
    tds = PyQuery(row).children('td').items()

    sunrise = get_hour(next(tds).text())
    sunset  = get_hour(next(tds).text())

    res.append([
        year,
        month,
        index + 1,
        sunrise,
        sunset,
    ])

if __name__ == '__main__':
    res = []

    for year in range(2008, 2013):
        for month in range(1, 13):
            pq = PyQuery(url='http://www.timeanddate.com/sun/mexico/veracruz?month=%d&year=%d'%(month, year))

            pq('#as-monthsun').find('tr[data-day]').each(lambda index, item: get_row(year, month, index, item, res))

            print('finished %d-%d'%(year, month))

    with open('data/sunrise_sunset.csv', 'w') as sunfile:
        writer = csv.writer(sunfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        writer.writerows(res)
