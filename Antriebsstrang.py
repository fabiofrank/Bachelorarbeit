import numpy as np
from scipy import constants
import Fahrer

# physikalische Konstanten
g = constants.g
luftdichte = 1.225  # in kg/m³

# feste Parameter
masse = 12000  # in kg
f_roll = 0.015  # Rollwiderstandbeiwert [ohne Einheit]
stirnflaeche = 8.8
c_w = 0.3  # Luftwiderstandsbeiwert

# Input: Ist-Geschwindigkeit in m/s, gewählte Beschleunigung in m/s² aus Fahrermodell
v_ist = 10.0
beschleunigung = Fahrer.gewählte_beschleunigung
steigung_prozent = 5
alpha = np.arctan(steigung_prozent / 100)


# Formeln der auftretenden Fahrwiderstände
def rollwiderstand():
    return masse * g * np.cos(alpha) * f_roll


def beschleunigungswiderstand():
    return masse * beschleunigung


def luftwiderstand():
    return 0.5 * stirnflaeche * c_w * luftdichte * (v_ist ** 2)


def steigungswiderstand():
    return masse * g * np.sin(alpha)


# Berechnung der zu überwindenden Fahrwiderstände
fahrwiderstaende = rollwiderstand() + beschleunigungswiderstand() + luftwiderstand() + steigungswiderstand()

# Berechnung der Leistung, die der Antriebsstrang benötigt unter Berücksichtigung von Verlusten im E-Motor
effizienz_elektromotor = 0.95
benoetigte_leistung = (fahrwiderstaende * v_ist) / effizienz_elektromotor # in Watt

print("Leistung, die vom Antriebsstrang benötigt wird: ", benoetigte_leistung, " Watt")
