import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#######################################################################################################################
# KONSTANTE LEISTUNG DER SONSTIGEN NEBENVERBRAUCHER (OHNE KLIMATISIERUNG/HEIZUNG) IN WATT

leistung_sonstiges = 6000 # Watt # Quelle: Berthold (2019), S. 56

#######################################################################################################################


# Aus Modelldaten des Primove-Projekts wird die Klimatisierungsleistung hergeleitet
inputdatei = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Fahrzeugkomponenten\Klimatisierungsdaten.xlsx'
daten_sommer = pd.read_excel(inputdatei, sheet_name='Sommertag')
daten_herbst = pd.read_excel(inputdatei, sheet_name='Herbsttag')
daten_winter = pd.read_excel(inputdatei, sheet_name='Wintertag')

# Winterdaten werden halbiert, da im betrachteten Bus mit einer deutlich effizienteren Heizug gearbeitet wird
# Symmetrie Sommer-Winter wird damit hergestellt
daten_ohneKorrektur = pd.concat([daten_sommer, daten_winter, daten_herbst]).sort_values(by='Außentemperatur [°C]')

daten_winter['Heizleistung Mittelwert [kW]'] = 0.5 * daten_winter['Heizleistung Mittelwert [kW]']
daten_kumuliert = pd.concat([daten_sommer, daten_winter, daten_herbst])
daten_geordnet = daten_kumuliert.sort_values(by='Außentemperatur [°C]')

temperatur = daten_geordnet['Außentemperatur [°C]'].to_numpy()
heizleistung = daten_geordnet['Heizleistung Mittelwert [kW]'].to_numpy()
heizleistung_ohneKorrektur = daten_ohneKorrektur['Heizleistung Mittelwert [kW]'].to_numpy()

fit = np.polyfit(temperatur, heizleistung, 2)
heizleistung_funktion = np.poly1d(fit)
heizleistung_funktion_ohneKorrektur = np.poly1d(np.polyfit(temperatur, heizleistung_ohneKorrektur, 2))

# x_new = np.arange(-15, 40)
# y_new = heizleistung_funktion(x_new)
#
# plt.plot(x_new, y_new)
# plt.plot(x_new, heizleistung_funktion_ohneKorrektur(x_new))
# plt.plot(temperatur, heizleistung_ohneKorrektur, 'ro')
# plt.plot(temperatur, heizleistung, 'ro')
#
# plt.show()

def leistung(gegebene_temperatur):
    global leistung_sonstiges
    leistung_klimatisierung = 1000 * heizleistung_funktion(gegebene_temperatur)  # in Watt
    return leistung_klimatisierung + leistung_sonstiges
