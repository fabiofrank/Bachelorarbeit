import numpy as np
from scipy import constants

# physikalische Konstanten
g = constants.g
luftdichte = 1.225 # in kg/m³

# feste Parameter
masse = 12000  # in kg
f_roll = 0.015  # Rollwiderstandbeiwert [ohne Einheit]
stirnflaeche = 8.8
c_w = 0.3  # Luftwiderstandsbeiwert

# Input: Ist-Geschwindigkeit in m/s, gewählte Beschleunigung in m/s² aus Fahrermodell
v_ist = 10.0
a_gewaehlt = 1.0
steigung_prozent = 5
alpha = np.arctan(steigung_prozent / 100)


def rollwiderstand():
    return masse * g * np.cos(alpha) * f_roll


def beschleunigungswiderstand():
    return masse * a_gewaehlt


def luftwiderstand():
    return 0.5 * stirnflaeche * c_w * luftdichte * (v_ist ** 2)


def steigungswiderstand():
    return masse * g * np.sin(alpha)


print("Rollwiderstand: ", rollwiderstand())
print("Beschleunigungswiderstand: ", beschleunigungswiderstand())
print("Luftwiderstand: ", luftwiderstand())
print("Steigungswiderstand: ", steigungswiderstand())

fahrwiderstaende = rollwiderstand() + beschleunigungswiderstand() + luftwiderstand() + steigungswiderstand()
benoetigte_leistung = fahrwiderstaende * v_ist
