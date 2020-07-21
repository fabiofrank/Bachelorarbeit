import numpy as np
from scipy import constants

# physikalische Konstanten
g = constants.g
luftdichte = 1.225  # in kg/m³, als konstant angenommen (eigentlich temperaturabhängig)

# feste Parameter, die zu Beginn der Simulation festgelegt werden müssen
masse: float  # in kg
f_roll: float  # Rollwiderstandskoeffizient[ohne Einheit]
stirnflaeche: float  # in qm
c_w: float  # Luftwiderstandsbeiwert


# Formeln der auftretenden Fahrwiderstände
def rollwiderstand(alpha):
    return masse * g * np.cos(alpha) * f_roll


def beschleunigungswiderstand(beschleunigung):
    return masse * beschleunigung


def luftwiderstand(v_ist):
    return 0.5 * stirnflaeche * c_w * luftdichte * (v_ist ** 2)


def steigungswiderstand(alpha):
    return masse * g * np.sin(alpha)


# Berechnung der zu überwindenden Fahrwiderstände
def fahrwiderstaende(v_ist, beschleunigung, steigung_in_prozent):
    alpha = np.arctan(steigung_in_prozent / 100)
    return rollwiderstand(alpha) + beschleunigungswiderstand(
        beschleunigung) + luftwiderstand(v_ist) + steigungswiderstand(alpha)
