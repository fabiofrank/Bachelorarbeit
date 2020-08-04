# TODO: Klimatisierungsdaten aus PRIMOVE integrieren
import Fahrer
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt

leistung = 10000

# daten_sommer = pd.read_excel('Klimatisierungsdaten.xlsx', sheet_name='Sommertag')
# daten_herbst = pd.read_excel('Klimatisierungsdaten.xlsx', sheet_name='Herbsttag')
# daten_winter = pd.read_excel('Klimatisierungsdaten.xlsx', sheet_name='Wintertag')
# daten_kumuliert = pd.concat([daten_sommer, daten_winter, daten_herbst])
# daten_geordnet = daten_kumuliert.sort_values(by='Außentemperatur [°C]')
#
# aussentemperatur = daten_geordnet['Außentemperatur [°C]'].to_numpy()
# heizleistung = daten_geordnet['Heizleistung Mittelwert [kW]'].to_numpy()
#
# heizleistung_interpoliert = interp1d(aussentemperatur, heizleistung)
#
# z = np.polyfit(aussentemperatur, heizleistung, 2)
# f = np.poly1d(z)
#
# x_new = np.arange(-20, 35)
# y_new = f(x_new)
#
# plt.plot(aussentemperatur, heizleistung, aussentemperatur,heizleistung_interpoliert(aussentemperatur), x_new, y_new)
# plt.show()
#
#
# leistung_klimatisierung = 10000  # in Watt
# leistung_sonstiges = 6000  # in Watt
#
# leistung = leistung_klimatisierung + leistung_sonstiges
