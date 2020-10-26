import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy

datei1 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_2Receiver.xlsx'
daten1 = pd.read_excel(datei1, sheet_name='Übersicht Betriebstag')
uhrzeit = daten1['Uhrzeit zu Beginn'].to_numpy()
soc1 = daten1['SoC zu Beginn [%]'].to_numpy()
for i in range(-28, 0):
    soc1[i] = 0
plt.plot_date(uhrzeit, soc1, fmt='o-', xdate=True, label='2 Empfängerspulen am Fahrzeug')

datei2= r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_3Receiver.xlsx'
daten2 = pd.read_excel(datei2, sheet_name='Übersicht Betriebstag')
soc2 = daten2['SoC zu Beginn [%]'].to_numpy()
for i in range(-21, 0):
    soc2[i] = 0
plt.plot(uhrzeit, soc2, label='3 Empfängerspulen am Fahrzeug')

datei3 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Basisszenario\Basisszenario_Linie24_ohneMittagspause.xlsx'
daten3 = pd.read_excel(datei3, sheet_name='Übersicht Betriebstag')
soc3 = daten3['SoC zu Beginn [%]'].to_numpy()
plt.plot(uhrzeit, soc3, label='4 Empfängerspulen am Fahrzeug (Basisszenario)')

datei4= r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_5Receiver.xlsx'
daten4 = pd.read_excel(datei4, sheet_name='Übersicht Betriebstag')
soc4 = daten4['SoC zu Beginn [%]'].to_numpy()
plt.plot(uhrzeit, soc4, label='5 Empfängerspulen am Fahrzeug')

datei5= r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_6Receiver.xlsx'
daten5 = pd.read_excel(datei5, sheet_name='Übersicht Betriebstag')
soc5 = daten5['SoC zu Beginn [%]'].to_numpy()
plt.plot(uhrzeit, soc5, label='6 Empfängerspulen am Fahrzeug')

plt.xticks(rotation=45)

ax.set_xlabel(r'$Uhrzeit \longrightarrow$', color='black')
ax.set_ylabel(r'$SoC$ / % $\longrightarrow$')
plt.title('Linie 24 - Variation der DWPT-Receiverzahl: 10,5 km Umlauf, davon 2,4 km DWPT-unterstützt / 174-kWh-Batterie (netto) / 15 Fahrgäste / 20 °C Außentemperatur')
plt.legend()
plt.show()