import numpy as np
from scipy import constants

# physikalische Konstanten
g = constants.g
luftdichte = 1.225  # in kg/m³

# feste Parameter, die zu Beginn der Simulation festgelegt werden müssen
masse = 0.0  # in kg
f_roll = 0.0  # Rollwiderstandbeiwert [ohne Einheit]
stirnflaeche = 0.0  # in qm
c_w = 0.0  # Luftwiderstandsbeiwert
effizienz_motor = 0.0
effizienz_getriebe = 0.0


# Formeln der auftretenden Fahrwiderstände
def rollwiderstand(alpha):
    return masse * g * np.cos(alpha) * f_roll


def beschleunigungswiderstand(beschleunigung):
    return masse * beschleunigung


def luftwiderstand(v_ist):
    return 0.5 * stirnflaeche * c_w * luftdichte * (v_ist ** 2)


def steigungswiderstand(alpha):
    return masse * g * np.sin(alpha)


def leistung(v_ist, beschleunigung, steigung_in_prozent):
    alpha = np.arctan(steigung_in_prozent / 100)

    # Berechnung der zu überwindenden Fahrwiderstände
    fahrwiderstaende = rollwiderstand(alpha) + beschleunigungswiderstand(
        beschleunigung) + luftwiderstand(v_ist) + steigungswiderstand(alpha)

    # Berechnung der Leistung, die der Antriebsstrang benötigt bzw. abgibt unter Berücksichtigung von Verlusten
    # TODO: Effizienzgrade einzeln ausweisen: EM, Getriebe, Leistungselektronik (99%), Batterie --> "Verluste"
    effizienz_antriebsstrang = effizienz_motor * effizienz_getriebe
    if fahrwiderstaende < 0:
        leistung = fahrwiderstaende * v_ist * effizienz_antriebsstrang
    else:
        leistung = (fahrwiderstaende * v_ist) / effizienz_antriebsstrang

    return leistung
