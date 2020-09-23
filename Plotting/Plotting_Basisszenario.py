import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
fig, ax = plt.subplots(1, 1)

datei1 = 'Outputdateien/Balingen/Linie 24/Basisszenario/Basisszenario_Linie24_inklMittagspause.xlsx'
daten1 = pd.read_excel(datei1, sheet_name='Übersicht Betriebstag')
uhrzeit = daten1['Uhrzeit zu Beginn'].to_numpy()
soc1 = daten1['SoC zu Beginn [%]'].to_numpy()
plt.plot(uhrzeit, soc1, 'o-', label='Basisszenario mit Mittagspause')

datei2 = 'Outputdateien/Balingen/Linie 24/Basisszenario/Basisszenario_Linie24_ohneMittagspause.xlsx'
daten2 = pd.read_excel(datei2, sheet_name='Übersicht Betriebstag')
soc2 = daten2['SoC zu Beginn [%]'].to_numpy()
plt.plot(uhrzeit, soc2, label='Basisszenario ohne Mittagspause')

plt.xticks(rotation=45)
ax.set_xlabel(r'$Uhrzeit \longrightarrow$', color='black')
ax.set_ylabel(r'$SoC$ / % $\longrightarrow$')
plt.title('Linie 24 - Basisszenario ("Good Case"): 10,5 km Umlauf, davon 2,4 km DWPT-unterstützt / 4 DWPT-Receiver / 174-kWh-Batterie (netto) / 15 Fahrgäste / 20 °C Außentemperatur')
plt.legend()
plt.show()