from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime

datei = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Basisszenario\Basisszenario_Linie24_inklMittagspause.xlsx'
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

fig, ax = plt.subplots(1, 1)
plt.plot_date(datetimes_array, soc_array, '-')
fmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(fmt)
plt.ylim(bottom=0)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
ax.set_xlabel(r'$Uhrzeit \longrightarrow$', color='black', fontsize=15)
ax.set_ylabel(r'$State\ of\ Charge$ / % $\longrightarrow$', fontsize=15)
plt.title(r'$\bf{Linie\ 24\ -\ Basisszenario}$' + '\n10,5 km Umlauf, davon 2,4 km DWPT-unterstützt / 4 DWPT-Receiver / 174-kWh-Batterie (netto) / 15 Fahrgäste / 20 °C Außentemperatur', fontsize=15)

plt.show()

