import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

def plot_settings():
    register_matplotlib_converters()
    plt.style.use('seaborn-white')
    plt.rcParams["figure.figsize"] = (11, 9)

def prepare_data(df):
    df_p = pd.DataFrame()
    df_p['t2m'] = df['t2m'].rolling(3, center=True).mean().round(1)
    df_p['wspd'] = df['wspd'].rolling(5, center=True).mean().round(1)
    df_p['cld'] = df['cld'].rolling(7, center=True).mean().round(1)
    df_p['ppr'] = df['ppr'].rolling(7, center=True).mean().round(1)
    df_p['spr'] = df['spr'].rolling(7, center=True).mean().round(1)
    df_p['wdir'] = round((57.3 * np.arctan2(df['u10'], df['v10']) + 180) / 45) * 45
    df_p['u10'] = df['u10'].rolling(3, center=True).mean().round(1)
    df_p['v10'] = df['v10'].rolling(3, center=True).mean().round(1)
    df_p['rpr'] = df_p['ppr'] - df_p['spr']

    df_p = df_p.head(100)
    df_p.dropna(inplace=True)

    df_p['ppr'] = df_p['ppr'].replace({0.0: np.nan, 0: np.nan})
    df_p['rpr'] = df_p['rpr'].replace({0.0: np.nan, 0: np.nan})
    df_p['spr'] = df_p['spr'].replace({0.0: np.nan, 0: np.nan})

    return df_p


def plot_data(df_p, develop):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

    ax1.plot(df_p['cld'], color='black', lw=1.7, alpha=0.2, label='Naoblaka')
    ax1.fill_between(df_p.index, 0, df_p['cld'], color='black', alpha=0.15)
    ax1.scatter(df_p.index, df_p['rpr'], marker='o', c='#3BBF28', s=22, alpha=1, label='Vjerojatnost kiše')
    ax1.scatter(df_p.index, df_p['spr'], marker='*', c='#005CA3', s=42, alpha=1, label='Vjerojatnost snijega')
    ax1.set_ylabel('%', fontsize=15)
    ax1.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
               mode="expand", borderaxespad=0, ncol=3)
    ax1.set_ylim([0, 103])
    ax1.axhline(y=0, color='black', lw=1)
    ax1.tick_params(axis='both', which='major', labelsize=14)
    ax1.grid(True)

    ax2.plot(df_p['t2m'], color='#5DA999', lw=1.7, alpha=0.8, label='Temperatura')
    ax2.fill_between(df_p.index, 0, df_p['t2m'], color='#5D9E68', alpha=0.15)
    ax2.set_ylabel('°C', fontsize=15)
    ax2.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
               mode="expand", borderaxespad=0, ncol=1)
    ax2.grid(True)
    ax2.axhline(y=0, color='blue', lw=2)
    ax2.set_ylim([min(df_p['t2m'] - 1), max(df_p['t2m'] + 1)])
    ax2.tick_params(axis='both', which='major', labelsize=14)

    ax3.plot(df_p['wspd'], color='#D91000', lw=1.7, alpha=0.8, label='Brzina vjetra')
    ax3.fill_between(df_p.index, 0, df_p['wspd'], color='#D91000', alpha=0.15)
    U = df_p['u10'] / np.sqrt(df_p['u10'] ** 2 + df_p['v10'] ** 2)
    V = df_p['v10'] / np.sqrt(df_p['u10'] ** 2 + df_p['v10'] ** 2)
    q = ax3.quiver(df_p.index[::3], (df_p['wspd'] / 2.5)[::3], U[::3], V[::3],
                   width=0.002, scale=40, alpha=0.7)
    ax3.quiverkey(q, X=0.905, Y=1.09, U=1.4, label='Smjer vjetra', labelpos='E')
    ax3.set_ylabel('m/s', fontsize=15)
    ax3.axhline(y=0, color='black', lw=1)
    # ax3.set_ylim([-1,max(df_p['wspd']+0.1*max(df_p['wspd']))])
    ax3.set_ylim([0, max(df_p['wspd'] + 0.1 * max(df_p['wspd']))])
    ax3.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
               mode="expand", borderaxespad=0, ncol=2)
    ax3.tick_params(axis='both', which='major', labelsize=14)
    ax3.grid(True)

    date_form_major = DateFormatter("%A \n %e.%m.%Y. \n 00:00")
    ax3.xaxis.set_major_formatter(date_form_major)
    ax3.xaxis.set_major_locator(mdates.DayLocator(interval=1))

    date_form_minor = DateFormatter("%H:00")
    ax3.xaxis.set_minor_formatter(date_form_minor)
    ax3.xaxis.set_minor_locator(mdates.HourLocator(12))

    if develop:
        plt.show()
    else:
        plt.savefig('/var/www/html/meteoadriatic/ezadar/plot.png')
