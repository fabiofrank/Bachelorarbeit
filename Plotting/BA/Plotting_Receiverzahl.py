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

datei2 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_2Receiver.xlsx'
datei3 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_3Receiver.xlsx'
datei4 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Basisszenario\Basisszenario_Linie24_ohneMittagspause.xlsx'
datei5 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_5Receiver.xlsx'
datei6 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_6Receiver.xlsx'


(x2, y2) = uhrzeit_soc_array(datei2)
(x3, y3) = uhrzeit_soc_array(datei3)
(x4, y4) = uhrzeit_soc_array(datei4)
(x5, y5) = uhrzeit_soc_array(datei5)
(x6, y6) = uhrzeit_soc_array(datei6)

def batterie_leer(y):
    index = 0
    for i in y:
        if i < 0.1:
            break
        index += 1

    for j in range(0,(len(y)-index)):
        y[index + j] = 0

batterie_leer(y2)
batterie_leer(y3)
batterie_leer(y4)
batterie_leer(y5)
batterie_leer(y6)

plt.plot_date(x2, y2, '-', label='2 Empfänger')
plt.plot_date(x3, y3, '-', label='3 Empfänger')
plt.plot_date(x4, y4, '-', label='4 Empfänger (Basis)')
plt.plot_date(x5, y5, '-', label='5 Empfänger')
plt.plot_date(x6, y6, '-', label='6 Empfänger')

fmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(fmt)
plt.ylim(bottom=0)
#plt.xticks(fontsize=12)
#plt.yticks(fontsize=12)
ax.set_xlabel(r'$Uhrzeit\ \longrightarrow$')
ax.set_ylabel(r'$SoC$ / % $\longrightarrow$')
plt.legend(borderpad=1)
#plt.title(r'$\bf{Linie\ 24\ -\ Basisszenario}$' + '\n10,5 km Umlauf, davon 2,4 km DWPT-unterstützt / 4 DWPT-Receiver / 174-kWh-Batterie (netto) / 15 Fahrgäste / 20 °C Außentemperatur', fontsize=15)
plt.grid()
fig.set_size_inches(7, 4)
fig.savefig(r'C:\Users\fabio\Studium\Bachelorarbeit\BA Latex\Latex_Bachelorarbeit\Bilder\SoC_Receiver.pgf')

#plt.show()