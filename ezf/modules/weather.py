import numpy as np
import random

def degToCompass(num):
    val = int((num / 22.5) + .5)
    # arr=["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    # return arr[(val % 16)]
    arr = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return arr[(val % 8)]


def tmin(t):
    tmin = t.between_time('04:30', '10:30').min().astype(int)
    return tmin


def tmax(t):
    tmax = t.between_time('10:30', '22:30').max().astype(int)
    return tmax


def wdir_am(u, v):
    u = u.between_time('04:30', '11:30').mean()
    v = v.between_time('04:30', '11:30').mean()
    wdir = (57.3 * np.arctan2(u, v) + 180).astype(int)
    wdirC = degToCompass(wdir)
    return wdirC


def wdir_pm(u, v):
    u = u.between_time('12:30', '22:30').mean()
    v = v.between_time('12:30', '22:30').mean()
    wdir = (57.3 * np.arctan2(u, v) + 180).astype(int)
    wdirC = degToCompass(wdir)
    return wdirC


def wspd_am(w):
    wspd = w.between_time('04:30', '11:30').mean().astype(int)
    return wspd


def wspd_pm(w):
    wspd = w.between_time('12:30', '22:30').mean().astype(int)
    return wspd

def mapping(wcode):
    '''
        *** Weather type logic ***

        Weather type codes:
        1 = clear ; 2 = nothing ; 3 = few clouds
        4 = scattered/broken clouds ; 5 = SCT/BKN with rain
        6 = SCT/BKN with sleet ; 7 = SCT/BKN with snow
        8 = overcast ; 9 = OVC with rain ; 10 = OVC with heavy rain
        11 = OVC with snow ; 12 = OVC with sleet
        13 = OVC with rain and tstorm ; 14 = fog
        15 = fog patches, mist, haze
        16 = OVC/BKN with rain and tstorm (showers)
    '''
    m = {  1: random.choice(['vedro vrijeme',
                             'pretežno vedro vrijeme']),
           3: random.choice(['malo oblačno vrijeme',
                             'pretežno vedro vrijeme uz slabu naoblaku',
                             'slaba naoblaka']),
           4: random.choice(['promjenjivo oblačno vrijeme',
                             'umjereno oblačno vrijeme',
                             'umjerena naoblaka']),
           5: random.choice(['promjenjivo oblačno vrijeme s kišom',
                             'promjenjivo oblačno vrijeme, povremeno uz kišu']),
           6: random.choice(['promjenjivo oblačno vrijeme s kišom i snijegom',
                             'promjenjivo oblačno vrijeme uz kišu, a moguć je i snijeg']),
           7: random.choice(['promjenjivo oblačno vrijeme sa snijegom',
                             'promjenjivo oblačno vrijeme, povremeno uz snijeg']),
           8: random.choice(['pretežno oblačno vrijeme',
                             'većinom oblačno vrijeme']),
           9: random.choice(['pretežno oblačno vrijeme i kišovito',
                             'pretežno oblačno vrijeme, povremeno uz kišu']),
           10: random.choice(['pretežno oblačno vrijeme uz veću količinu kiše',
                              'pretežno oblačno vrijeme uz kišu, moguće i obilniju']),
           11: random.choice(['pretežno oblačno vrijeme sa snijegom',
                              'pretežno oblačno vrijeme, povremeno uz snijeg']),
           12: random.choice(['pretežno oblačno vrijeme s povremenom kišom i snijegom',
                              'pretežno oblačno vrijeme, povremeno uz oborinu na granici kiše i snijega']),
           13: random.choice(['pretežno oblačno vrijeme s kišom i grmljavinom',
                              'pretežno oblačno vrijeme s kišom, povremeno uz grmljavinu']),
           14: random.choice(['maglovito vrijeme',
                              'tmurno i maglovito vrijeme']),
           15: random.choice(['malo oblačno vrijeme ali ponegdje i maglovito',
                              'malo oblačno vrijeme ali uz moguću sumaglicu ili maglu']),
           16: random.choice(['promjenjivo oblačno vrijeme uz mogućnost kratkotrajne kiše i grmljavine',
                              'promjenjivo oblačno vrijeme uz moguć grmljavinski pljusak']), }
    return m[wcode]


def tdiff(first_day_tmin, first_day_tmax, second_day_tmin, second_day_tmax):
    tdiff_min = int(second_day_tmin) - int(first_day_tmin)
    tdiff_max = int(second_day_tmax) - int(first_day_tmax)
    tdiff_txt = ''
    if tdiff_min < -1 and tdiff_max < -1:
        tdiff_txt = random.choice(['Malo hladnije. ', 'Malo će zahladiti. '])
    if tdiff_min < -3 and tdiff_max < -3:
        tdiff_txt = random.choice(['Hladnije. ', 'Zahladit će. '])
    if tdiff_min < -5 and tdiff_max < -5:
        tdiff_txt = random.choice(['Znatno hladnije. ', 'Znatno će zahladiti. '])
    if tdiff_min > 1 and tdiff_max > 1:
        tdiff_txt = random.choice(['Malo toplije. ', 'Malo će zatopliti. '])
    if tdiff_min > 3 and tdiff_max > 3:
        tdiff_txt = random.choice(['Toplije. ', 'Zatoplit će. '])
    if tdiff_min > 5 and tdiff_max > 5:
        tdiff_txt = random.choice(['Znatno toplije. ', 'Znatno će zatopliti. '])
    return tdiff_txt