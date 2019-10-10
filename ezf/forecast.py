
# Planning to run two forecast updates/day.
#
# "Morning" forecast will run soon after midnight
# "Afternoon" forecast will run somewhere during PM hours
#
# "Morning" fcst will not have all morning elements for first day,
# for example minimum temperature will be left out. It will
# contain forecast for the rest of that day and for tomorrow.
#
# "Afternoon" fcst will contain forecast for next day and day after.

from dotenv import load_dotenv
import os, locale, random
import datetime as dt
from string import Template

from ezf.modules.argument_parser import argument_parser
from ezf.modules.read_data import read_csv
from ezf.modules.dates import get_fdays
from ezf.modules.weather import temp, wdir, wspd, tdiff, weather_c2t_mapping
from ezf.modules.lut import weather_lut
from ezf.modules.plotting import plot_settings, prepare_data, plot_data

load_dotenv()
root = os.getenv('PROJECT_FOLDER')
develop = os.getenv('DEVELOP')

locale.setlocale(locale.LC_ALL, 'hr_HR.UTF-8')

def run():
    forecastt = argument_parser()

    # Fresh file available at https://gamma.meteoadriatic.net/meteoadriatic/homepage/data/Zadar.csv
    df = read_csv(os.path.join(root, 'data/Zadar.csv'))

    fday1, fday2 = get_fdays(forecastt)
    print(fday1, fday2)

    def weather(data, period):
        wtxt = []
        if period == 'am':
            p_start = '05:30'
            p_end = '12:30'
        else:
            p_start = '12:30'
            p_end = '22:30'

        for i in data:
            p_mean = i.between_time(p_start, p_end).mean()
            p_max = i.between_time(p_start, p_end).max()
            wt = weather_c2t_mapping(weather_lut(p_mean, p_max))
            wtxt.append(wt)

        return (wtxt)

    if forecastt == 'morning':
        day1 = "danas"
        day2 = "sutra"
    else:
        day1 = "sutra"
        day2 = "preksutra"

    tmin = temp([df.loc[fday1]['t2m'], df.loc[fday2]['t2m']], 'min')
    tmax = temp([df.loc[fday1]['t2m'], df.loc[fday2]['t2m']], 'max')
    wdir_am = wdir([df.loc[fday1]['u10'], df.loc[fday1]['v10']], [df.loc[fday2]['u10'], df.loc[fday2]['u10']], 'am')
    wdir_pm = wdir([df.loc[fday1]['u10'], df.loc[fday1]['v10']], [df.loc[fday2]['u10'], df.loc[fday2]['u10']], 'pm')
    wspd_am = wspd([df.loc[fday1]['wspd'], df.loc[fday2]['wspd']], 'am')
    wspd_pm = wspd([df.loc[fday1]['wspd'], df.loc[fday2]['wspd']], 'pm')
    weather_am = weather([df.loc[fday1], df.loc[fday2]], 'am')
    weather_pm = weather([df.loc[fday1], df.loc[fday2]], 'pm')

    tdiff_txt = tdiff(tmin[0], tmax[0], tmin[1], tmax[1])


    ### FIRST DAY ###
    #################
    template_dir = os.path.join(os.path.join(root, 'templates'), forecastt)

    if weather_am[0] != weather_pm[0]:
        ttype = 'type1.txt'
    else:
        ttype = 'type2.txt'

    random_template = random.choice([
        x for x in os.listdir(template_dir)
        if os.path.isfile(os.path.join(template_dir, x)) and
           x.endswith(ttype)
    ])
    template = os.path.join(template_dir, random_template)
    rt1 = random_template

    with open(template, 'r') as tf:
        content = tf.read()

    t = Template(content)

    if forecastt == 'morning':
        forecast_first_day = t.substitute(day=day1,
                                         weather_am=weather_am[0],
                                         weather_pm=weather_pm[0],
                                         tmax=tmax[0])
    else:
        forecast_first_day = t.substitute(day=day1,
                                         weather_am=weather_am[0],
                                         weather_pm=weather_pm[0],
                                         tdiff_txt='',
                                         tmin=tmin[0],
                                         tmax=tmax[0])

    forecast_first_day = ''.join(forecast_first_day.rsplit(' vrijeme', 1)) # avoid duplicate " vrijeme" string
    forecast_first_day = forecast_first_day[0].upper() + forecast_first_day[1:] # capitalize first letter

    ### SECOND DAY ###
    ##################
    # Note: For second day we always use "afternoon" template type
    template_dir = os.path.join(os.path.join(root, 'templates'), 'afternoon')

    if weather_am[1] != weather_pm[1]:
        ttype = 'type1.txt'
    else:
        ttype = 'type2.txt'

    while True:
        random_template = random.choice([
            x for x in os.listdir(template_dir)
            if os.path.isfile(os.path.join(template_dir, x)) and
               x.endswith(ttype)
        ])
        if random_template != rt1:
            break

    template = os.path.join(template_dir, random_template)
    #rt2 = random_template

    with open(template, 'r') as tf:
        content = tf.read()

    t = Template(content)

    forecast_second_day = t.substitute(day=day2,
                                      weather_am=weather_am[1],
                                      weather_pm=weather_pm[1],
                                      tdiff_txt=tdiff_txt,
                                      tmin=tmin[1],
                                      tmax=tmax[1])

    forecast_second_day = ''.join(forecast_second_day.rsplit(' vrijeme', 1)) # avoid duplicate " vrijeme" string
    forecast_second_day = forecast_second_day[0].upper() + forecast_second_day[1:] # capitalize first letter

    date1 = (dt.datetime.strptime(fday1, "%Y-%m-%d")).strftime("%e.%m.%Y. (%A)").strip()
    date2 = (dt.datetime.strptime(fday2, "%Y-%m-%d")).strftime("%e.%m.%Y. (%A)").strip()

    intro = "Vremenska prognoza za Zadar"
    outro = "Računalno generirana prognoza by meteoadriatic.net"

    forecast = intro + '\n' + '\n' + \
               date1 + '\n' + \
               forecast_first_day + '\n' + \
               date2 + '\n' + \
               forecast_second_day + '\n' + '\n' + \
               outro

    print(forecast)

    if develop:
        pass
    else:
        f = open("/var/www/html/meteoadriatic/ezadar/prognoza.txt", "w+")
        f.write(forecast)
        f.close()

    # Create plot
    plot_settings()
    df_p = prepare_data(df)
    plot_data(df_p, develop)



if __name__== "__main__":
    run()