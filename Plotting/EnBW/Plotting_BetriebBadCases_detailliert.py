from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime

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
datei2 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Fahrgastaufkommen\Linie24_30Fahrgaeste.xlsx'
datei3 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Kein Halt auf Tübinger Str\Linie24_keinHaltaufTuebingerStr.xlsx'

(x1, y1) = uhrzeit_soc_array(datei1)
(x2, y2) = uhrzeit_soc_array(datei2)
(x3, y3) = uhrzeit_soc_array(datei3)

plt.plot_date(x1, y1, '-', label='Basisszenario')
plt.plot_date(x2, y2, '-', label='30 Fahrgäste pro Fahrt')
plt.plot_date(x3, y3, '-', label='Kein Halt auf DWPT-unterstützter Tübinger Str.')

fmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(fmt)
plt.ylim(bottom=0)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
ax.set_xlabel(r'$Uhrzeit\ \longrightarrow$', color='black', fontsize=15)
ax.set_ylabel(r'$State\ of\ Charge$ / % $\longrightarrow$', fontsize=15)
plt.legend()
#plt.title(r'$\bf{Linie\ 24\ -\ Basisszenario}$' + '\n10,5 km Umlauf, davon 2,4 km DWPT-unterstützt / 4 DWPT-Receiver / 174-kWh-Batterie (netto) / 15 Fahrgäste / 20 °C Außentemperatur', fontsize=15)
plt.show()
