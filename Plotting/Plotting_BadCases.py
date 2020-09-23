import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
fig, ax = plt.subplots(1, 1)

# plot your data here ...
datei5 = 'Outputdateien/Balingen/Linie 24/Basisszenario/Basisszenario_Linie24_inklMittagspause.xlsx'
daten5 = pd.read_excel(datei5, sheet_name='Übersicht Betriebstag')
uhrzeit = daten5['Uhrzeit zu Beginn'].to_numpy()
soc5 = daten5['SoC zu Beginn [%]'].to_numpy()
plt.plot(uhrzeit, soc5, label='Basisszenario: 15 Fahrgäste, 20 °C Außentemperatur')

datei1 = 'Outputdateien/Balingen/Linie 24/Fahrgastaufkommen/Linie24_30Fahrgaeste.xlsx'
daten1 = pd.read_excel(datei1, sheet_name='Übersicht Betriebstag')
soc1 = daten1['SoC zu Beginn [%]'].to_numpy()
plt.plot(uhrzeit, soc1, label='erhöhtes Fahrgastaufkommen (30 Passagiere pro Fahrt)')

datei2 = 'Outputdateien/Balingen/Linie 24/Temperatureinfluss/Linie24_kalterWintertag.xlsx'
daten2 = pd.read_excel(datei2, sheet_name='Übersicht Betriebstag')
soc2 = daten2['SoC zu Beginn [%]'].to_numpy()
plt.plot(uhrzeit, soc2, label='kalter Wintertag (-10 °C)')

datei3 = 'Outputdateien/Balingen/Linie 24/Kein Halt auf Tübinger Str/Linie24_keinHaltaufTuebingerStr.xlsx'
daten3 = pd.read_excel(datei3, sheet_name='Übersicht Betriebstag')
soc3 = daten3['SoC zu Beginn [%]'].to_numpy()
plt.plot(uhrzeit, soc3, label='kein Halt auf DWPT-unterstützter Tübinger Str.')

datei4 = 'Outputdateien/Balingen/Linie 24/Worst Case/Linie24_WorstCase.xlsx'
daten4 = pd.read_excel(datei4, sheet_name='Übersicht Betriebstag')
soc4 = daten4['SoC zu Beginn [%]'].to_numpy()
soc4[-1] = 0.0
soc4[-2] = 0.0
soc4[-3] = 0.0
soc4[-4] = 0.0
soc4[-5] = 0.0
soc4[-6] = 0.0
plt.plot(uhrzeit, soc4, label='Worst Case (Kombination der 3 "Bad Cases")')



plt.xticks(rotation=45)
ax.set_xlabel(r'$Uhrzeit \longrightarrow$', color='black')
ax.set_ylabel(r'$SoC$ / % $\longrightarrow$')
plt.title('Linie 24 - "Bad Cases", für alle gilt: 10,5 km Umlauf, davon 2,4 km DWPT-unterstützt / 4 DWPT-Receiver / 174-kWh-Batterie (netto)')
plt.legend()
plt.show()