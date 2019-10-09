def weather_lut(pmean, pmax):
    
    wcode = 1
    if pmean['cld'] > 15: wcode = 3
    if pmean['cld'] > 35: wcode = 4
    if pmean['cld'] > 85: wcode = 8
    if pmean['prec'] > 0.02: wcode = 9
    if wcode == 9 and pmean['cld'] < 85: wcode = 5
    if pmean['prec'] > 1.5: wcode = 10
    if (wcode == 9 or wcode == 10) and pmax['tpr'] > 50: wcode = 13
    if wcode == 5 and pmax['tpr'] > 50: wcode = 16
    if (wcode == 9 or wcode == 10) and pmax['spr'] > 0.2 * pmax['ppr']: wcode = 11
    if wcode == 11 and pmax['spr'] < 0.7 * pmax['ppr']: wcode = 12
    if wcode == 5 and pmax['spr'] > 0.2 * pmax['ppr']: wcode = 7
    if wcode == 7 and pmax['spr'] < 0.7 * pmax['ppr']: wcode = 6
    if (wcode == 1 or wcode == 3 or wcode == 4 or wcode == 8) and (
            pmean['h2m'] > 97 and pmax['h2m'] > 99): wcode = 14
    if (wcode == 1 or wcode == 3 or wcode == 4) and (pmean['h2m'] > 90 and pmax['h2m'] > 95): wcode = 15
    
    return wcode