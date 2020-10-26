import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
fig, ax = plt.subplots(1, 1)

datei2 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Rundkurs für Gartenschau\reale Umsetzung\Gartenschau_ohneMessegelände_50Fahrgaeste_35Grad.xlsx'
daten2 = pd.read_excel(datei2, sheet_name='Übersicht Betriebstag')
uhrzeit = daten2['Uhrzeit zu Beginn'].to_numpy()
soc2 = daten2['SoC zu Beginn [%]'].to_numpy()
soc2[-1] = 0.0
soc2[-2] = 0.0
soc2[-3] = 0.0
soc2[-4] = 0.0
soc2[-5] = 0.0
plt.plot(uhrzeit, soc2, label='insgesamt 900 m DWPT-Strecke an Anfang und Ende der Route')

datei1 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Rundkurs für Gartenschau\reale Umsetzung\Gartenschau_inklMessegelände_50Fahrgaeste_35Grad.xlsx'
daten1 = pd.read_excel(datei1, sheet_name='Übersicht Betriebstag')

soc1 = daten1['SoC zu Beginn [%]'].to_numpy()
plt.plot(uhrzeit, soc1, label='zusätzliche DWPT-Zone am Messegelände (2-minütiger Halt), insgesamt 1000 m')

plt.title('Rundkurs Gartenschau - "Bad Case": 5,9 km Umlauf / 4 DWPT-Receiver / 174-kWh-Batterie (netto) / 50 Fahrgäste / 35 °C Außentemperatur')
plt.xticks(rotation=45)
ax.set_xlabel(r'$Uhrzeit \longrightarrow$', color='black')
ax.set_ylabel(r'$SoC$ / % $\longrightarrow$')
plt.legend()
plt.show()