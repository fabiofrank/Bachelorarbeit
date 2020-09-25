import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
fig, ax = plt.subplots(1, 1)

datei1 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Basisszenario\Basisszenario_Linie24_inklMittagspause.xlsx'
daten1 = pd.read_excel(datei1, sheet_name='3 Umlauf')
uhrzeit = daten1['Uhrzeit'].to_numpy()
soc1 = daten1['SoC zum Zeitpunkt t \n[%]'].to_numpy()
plt.plot(uhrzeit, soc1, label='Basisszenario mit Mittagspause')


ax.set_xlabel(r'$Uhrzeit \longrightarrow$', color='black')
ax.set_ylabel(r'$SoC$ / % $\longrightarrow$')
plt.xticks(rotation=45)
plt.title('Linie 24 - Basisszenario ("Good Case"): 10,5 km Umlauf, davon 2,4 km DWPT-unterstützt / 4 DWPT-Receiver / 174-kWh-Batterie (netto) / 15 Fahrgäste / 20 °C Außentemperatur')
plt.legend()
plt.show()