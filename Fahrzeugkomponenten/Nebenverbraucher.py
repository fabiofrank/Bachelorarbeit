# TODO: plausibler Fit?

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt

inputdatei = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Fahrzeugkomponenten\Klimatisierungsdaten.xlsx'
daten_sommer = pd.read_excel(inputdatei, sheet_name='Sommertag')
daten_herbst = pd.read_excel(inputdatei, sheet_name='Herbsttag')
daten_winter = pd.read_excel(inputdatei, sheet_name='Wintertag')
daten_kumuliert = pd.concat([daten_sommer ,daten_winter, daten_herbst])
daten_geordnet = daten_kumuliert.sort_values(by='Außentemperatur [°C]')

aussentemperatur = daten_geordnet['Außentemperatur [°C]'].to_numpy()
heizleistung = daten_geordnet['Heizleistung Mittelwert [kW]'].to_numpy()

z = np.polyfit(aussentemperatur, heizleistung, 2)
f = np.poly1d(z)

x_new = np.arange(-15, 40)
y_new = f(x_new)

plt.plot(x_new, y_new)
plt.plot(aussentemperatur, heizleistung, 'ro')
plt.show()

def leistung(gegebene_temperatur):
    leistung_klimatisierung = f(gegebene_temperatur)  # in Watt
    leistung_sonstiges = 6000  # in Watt
    return leistung_klimatisierung + leistung_sonstiges
