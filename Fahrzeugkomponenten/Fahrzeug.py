import numpy as np
from scipy import constants

# KONSTANTE PARAMETER, DIE FÜR DIE SIMULATION FESTGELEGT WERDEN MÜSSEN

# Leergewicht des Fahrzeugs in kg
masse_leer = 12760

# Frontfäche des Fahrzeugs in qm
stirnflaeche = 8.6649

# Anzahl an DWPT-Empfängerspulen am Fahrzeug
anzahl_spulen = 3

# Anzahl an Fahrgästen
anzahl_fahrgaeste: int # Higer-Bus: Max. 90 Passagiere

#############################################################################################

# Annahmen
f_roll: float  # Rollwiderstandskoeffizient[ohne Einheit]
c_w: float  # Luftwiderstandsbeiwert
masse_je_fahrgast = 77.8  # in kg, Mittleres Körpergewicht von Erwerbstätigen in Deutschland = 77.8 kg

# physikalische Konstanten
g = constants.g
luftdichte = 1.225  # in kg/m³, als konstant angenommen


# Masse in Abhängigkeit von Leergewicht und Fahrgastaufkommen
def masse():
    return masse_leer + anzahl_fahrgaeste * masse_je_fahrgast


# Formeln der auftretenden Fahrwiderstände
def rollwiderstand(alpha):
    return masse() * g * np.cos(alpha) * f_roll


# TODO: m_acc berücksichtigen oder mit Faktor multiplizieren
def beschleunigungswiderstand(beschleunigung):
    return masse() * beschleunigung


def luftwiderstand(v_ist):
    return 0.5 * stirnflaeche * c_w * luftdichte * (v_ist ** 2)


def steigungswiderstand(alpha):
    return masse() * g * np.sin(alpha)


# Berechnung der zu überwindenden Fahrwiderstände
def fahrwiderstaende(v_ist, beschleunigung, steigung_in_prozent):
    alpha = np.arctan(steigung_in_prozent / 100)
    return rollwiderstand(alpha) + beschleunigungswiderstand(
        beschleunigung) + luftwiderstand(v_ist) + steigungswiderstand(alpha)
