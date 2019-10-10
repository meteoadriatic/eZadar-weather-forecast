
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
import os, locale, random, argparse
import datetime as dt
from string import Template

from ezf.modules.read_data import read_csv
from ezf.modules.dates import get_dates
from ezf.modules.weather import tmin, tmax, wdir_am, wdir_pm, wspd_am, wspd_pm
from ezf.modules.lut import weather_lut
from ezf.modules.weather import mapping
from ezf.modules.plotting import plot_settings, prepare_data, plot_data
from ezf.modules.weather import tdiff

load_dotenv()
root = os.getenv('PROJECT_FOLDER')
develop = os.getenv('DEVELOP')

locale.setlocale(locale.LC_ALL, 'hr_HR.UTF-8')

def run():
    parser = argparse.ArgumentParser(description='Arg parser')
    parser.add_argument("--forecast",
                        choices=["morning", "afternoon"],
                        required=True, type=str, help="Forecast time")

    args = parser.parse_args()
    forecastt = args.forecast

    # Fresh file available at https://gamma.meteoadriatic.net/meteoadriatic/homepage/data/Zadar.csv
    df = read_csv(os.path.join(root, 'data/Zadar.csv'))
    d0, d1, d2 = get_dates()

    # Obtain statistics for requested periods
    def weather_code(data):
        weather_am = ''
        weather_pm = ''
        periods = [['am', '05:30', '12:30'],
                   ['pm', '12:30', '22:30']]
        for period in periods:
            p_name = period[0]
            p_start = period[1]
            p_end = period[2]
            p_mean = data.between_time(p_start, p_end).mean()
            p_max = data.between_time(p_start, p_end).max()

            if p_name == 'am': weather_am = mapping(weather_lut(p_mean, p_max))
            if p_name == 'pm': weather_pm = mapping(weather_lut(p_mean, p_max))
        return (weather_am, weather_pm)

    if forecastt == 'morning':
        day1 = "danas"
        first_day_tmin = tmin(df.loc[d0]['t2m'])
        first_day_tmax = tmax(df.loc[d0]['t2m'])
        first_day_wdir_am = wdir_am(df.loc[d0]['u10'], df.loc[d0]['v10'])
        first_day_wdir_pm = wdir_pm(df.loc[d0]['u10'], df.loc[d0]['v10'])
        first_day_wspd_am = wspd_am(df.loc[d0]['wspd'])
        first_day_wspd_pm = wspd_pm(df.loc[d0]['wspd'])
        first_day_weather_am = weather_code(df.loc[d0])[0]
        first_day_weather_pm = weather_code(df.loc[d0])[1]

        day2 = "sutra"
        second_day_tmin = tmin(df.loc[d1]['t2m'])
        second_day_tmax = tmax(df.loc[d1]['t2m'])
        second_day_wdir_am = wdir_am(df.loc[d1]['u10'], df.loc[d1]['v10'])
        second_day_wdir_pm = wdir_pm(df.loc[d1]['u10'], df.loc[d1]['v10'])
        second_day_wspd_am = wspd_am(df.loc[d1]['wspd'])
        second_day_wspd_pm = wspd_pm(df.loc[d1]['wspd'])
        second_day_weather_am = weather_code(df.loc[d1])[0]
        second_day_weather_pm = weather_code(df.loc[d1])[1]

    else:
        day1 = "sutra"
        first_day_tmin = tmin(df.loc[d1]['t2m'])
        first_day_tmax = tmax(df.loc[d1]['t2m'])
        first_day_wdir_am = wdir_am(df.loc[d1]['u10'], df.loc[d1]['v10'])
        first_day_wdir_pm = wdir_pm(df.loc[d1]['u10'], df.loc[d1]['v10'])
        first_day_wspd_am = wspd_am(df.loc[d1]['wspd'])
        first_day_wspd_pm = wspd_pm(df.loc[d1]['wspd'])
        first_day_weather_am = weather_code(df.loc[d1])[0]
        first_day_weather_pm = weather_code(df.loc[d1])[1]

        day2 = "preksutra"
        second_day_tmin = tmin(df.loc[d2]['t2m'])
        second_day_tmax = tmax(df.loc[d2]['t2m'])
        second_day_wdir_am = wdir_am(df.loc[d2]['u10'], df.loc[d2]['v10'])
        second_day_wdir_pm = wdir_pm(df.loc[d2]['u10'], df.loc[d2]['v10'])
        second_day_wspd_am = wspd_am(df.loc[d2]['wspd'])
        second_day_wspd_pm = wspd_pm(df.loc[d2]['wspd'])
        second_day_weather_am = weather_code(df.loc[d2])[0]
        second_day_weather_pm = weather_code(df.loc[d2])[1]

    tdiff_txt = tdiff(first_day_tmin, first_day_tmax, second_day_tmin, second_day_tmax)


    ### FIRST DAY ###
    #################
    template_dir = os.path.join(os.path.join(root, 'templates'), forecastt)

    if first_day_weather_am != first_day_weather_pm:
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
                                         weather_am=first_day_weather_am,
                                         weather_pm=first_day_weather_pm,
                                         tmax=first_day_tmax)
    else:
        forecast_first_day = t.substitute(day=day1,
                                         weather_am=first_day_weather_am,
                                         weather_pm=first_day_weather_pm,
                                         tdiff_txt='',
                                         tmin=first_day_tmin,
                                         tmax=first_day_tmax)

    forecast_first_day = ''.join(forecast_first_day.rsplit(' vrijeme', 1))

    ### SECOND DAY ###
    ##################
    # Note: For second day we always use "afternoon" template type
    template_dir = os.path.join(os.path.join(root, 'templates'), 'afternoon')

    if second_day_weather_am != second_day_weather_pm:
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
                                      weather_am=second_day_weather_am,
                                      weather_pm=second_day_weather_pm,
                                      tdiff_txt=tdiff_txt,
                                      tmin=second_day_tmin,
                                      tmax=second_day_tmax)

    forecast_second_day = ''.join(forecast_second_day.rsplit(' vrijeme', 1))

    if forecastt == 'morning':
        date1 = (dt.datetime.strptime(d0, "%Y-%m-%d")).strftime("%e.%m.%Y. (%A)").strip()
        date2 = (dt.datetime.strptime(d1, "%Y-%m-%d")).strftime("%e.%m.%Y. (%A)").strip()
    else:
        date1 = (dt.datetime.strptime(d1, "%Y-%m-%d")).strftime("%e.%m.%Y. (%A)").strip()
        date2 = (dt.datetime.strptime(d2, "%Y-%m-%d")).strftime("%e.%m.%Y. (%A)").strip()

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