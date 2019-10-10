import numpy as np
import random

def degToCompass(num):
    val = int((num / 22.5) + .5)
    # arr=["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    # return arr[(val % 16)]
    arr = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return arr[(val % 8)]

def temp(t, extremum):
    temp = []
    if extremum == 'min':
        p_start = '04:30'
        p_end = '10:30'
    else:
        p_start = '10:30'
        p_end = '22:30'
    for i in t:
        tmp = i.between_time(p_start, p_end).max().astype(int)
        temp.append(tmp)
    return temp

def wdir(u, v, period):
    wdirC = []
    if period == 'am':
        p_start = '05:30'
        p_end = '12:30'
    else:
        p_start = '12:30'
        p_end = '22:30'
    for i in (u, v):
        uu = i[0].between_time(p_start, p_end).mean()
        vv = i[1].between_time(p_start, p_end).mean()
        wd = (57.3 * np.arctan2(uu, vv) + 180).astype(int)
        wC = degToCompass(wd)
        wdirC.append(wC)
    return wdirC

def wspd(w, period):
    wspd = []
    if period == 'am':
        p_start = '05:30'
        p_end = '12:30'
    else:
        p_start = '12:30'
        p_end = '22:30'
    for i in w:
        ws = i.between_time(p_start, p_end).min().astype(int)
        wspd.append(ws)
    return wspd

def weather_c2t_mapping(wcode):
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
