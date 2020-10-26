import matplotlib
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    #'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    'pgf.preamble': [
        r"\usepackage[latin1]{inputenc}",    # use utf8 fonts
        r"\usepackage[T1]{fontenc}",        # plots will be generated
        r"\usepackage[detect-all,locale=DE]{siunitx}",
        ]
})

def uhrzeit_soc_array(datei):
    daten_dict = pd.read_excel(datei, sheet_name=None)
    del daten_dict['Übersicht Betriebstag']
    del daten_dict['Parameter']

    liste = []
    soc_array = np.array(liste)
    uhrzeit_array = np.array([])

    for tabellenblatt in daten_dict:
        umlauf_dataframe = daten_dict[tabellenblatt]
        uhrzeit_umlauf = umlauf_dataframe['Uhrzeit']
        uhrzeit_array = np.append(uhrzeit_array, uhrzeit_umlauf)
        uhrzeit_format = mdates.DateFormatter('%H:%M')

        if 'Umlauf' in tabellenblatt:
            soc_umlauf = umlauf_dataframe['SoC zum Zeitpunkt t \n[%]'].to_numpy()
        elif 'Pause' in tabellenblatt:
            soc_umlauf = umlauf_dataframe['SoC [%]'].to_numpy()
        soc_array = np.append(soc_array, soc_umlauf)

    datetimes_liste = []
    for i in range(0, len(uhrzeit_array)):
        datetimes_liste.append(datetime.strptime(uhrzeit_array[i], '%H:%M:%S'))
    datetimes_array = np.array(datetimes_liste)
    return (datetimes_array, soc_array)

################################################################################################################################
fig, ax = plt.subplots(1, 1)

datei1 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Basisszenario\Basisszenario_Linie24_inklMittagspause.xlsx'
datei2 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Temperatureinfluss\Linie24_kalterWintertag.xlsx'
datei3 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Temperatureinfluss\Linie24_heisserSommertag.xlsx'
datei4 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Temperatureinfluss\ohneHVAC.xlsx'

(x1, y1) = uhrzeit_soc_array(datei1)
(x2, y2) = uhrzeit_soc_array(datei2)
(x3, y3) = uhrzeit_soc_array(datei3)
(x4, y4) = uhrzeit_soc_array(datei4)

def batterie_leer(y):
    index = 0
    for i in y:
        if i < 0.1:
            break
        index += 1

    for j in range(0,(len(y)-index)):
        y[index + j] = 0

batterie_leer(y1)
batterie_leer(y2)
batterie_leer(y3)

plt.plot_date(x1, y1, '-', label='\SI{20}{\degreeCelsius} (Basis)', zorder=2)
plt.plot_date(x2, y2, '-', label='\SI{-10}{\degreeCelsius} (C)', zorder=3)
plt.plot_date(x3, y3, '.-', markevery=900, label='\SI{35}{\degreeCelsius}', zorder=1)
plt.plot_date(x4, y4, ':', color='0.5', label='ohne HVAC', zorder=0)

fmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(fmt)
plt.ylim(bottom=0)
ax.set_xlabel(r'$Uhrzeit\ \longrightarrow$')
ax.set_ylabel(r'$SoC$ / % $\longrightarrow$')
plt.legend()
plt.grid()
fig.set_size_inches(7, 4)
fig.savefig(r'C:\Users\fabio\Studium\Bachelorarbeit\BA Latex\Latex_Bachelorarbeit\Bilder\SoC_Aussentemperatur.pgf')