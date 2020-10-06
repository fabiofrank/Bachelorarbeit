import numpy as np
from scipy import constants

#######################################################################################################################
# KONSTANTE PARAMETER, DIE FÜR DIE SIMULATION FESTGELEGT WERDEN MÜSSEN

# Leergewicht des Fahrzeugs in kg
masse_leer = 12760

# Frontfäche des Fahrzeugs in qm
stirnflaeche = 8.6649



# Mittleres Fahrgastgewicht in kg, abhängig von Kunden des Busbetriebs
masse_je_fahrgast = 77.0  # Mittleres Körpergewicht von Erwerbstätigen in Deutschland = 77.8 kg
                          # Mittleres Körpergewicht eines Erwachsenen in Deutschland = 77.0 kg

# Rollwiderstandskoeffizient[ohne Einheit], konstant angenommen
f_roll = 0.015

# Luftwiderstandsbeiwert
c_w = 0.66

#######################################################################################################################


# physikalische Konstanten
g = constants.g  # Erdbeschleunigung in m/s²
luftdichte = 1.225  # in kg/m³, als konstant angenommen

# Anzahl an Fahrgästen (wird durch Umlauf übergeben)
anzahl_fahrgaeste: int  # Higer-Bus: Max. 90 Passagiere

# Masse in Abhängigkeit von Leergewicht und Fahrgastaufkommen
def masse():
    return masse_leer + anzahl_fahrgaeste * masse_je_fahrgast


# Formeln der auftretenden Fahrwiderstände
def rollwiderstand(alpha):
    return masse() * g * np.cos(alpha) * f_roll


def beschleunigungswiderstand(beschleunigung):
    massenfaktor = 1.05 # berücksichtigt rotatorische Trägheit
    zusatzmasse = anzahl_fahrgaeste * masse_je_fahrgast # Masse der Fahrgäste
    return (massenfaktor * masse_leer + zusatzmasse) * beschleunigung


def luftwiderstand(v_ist):
    return 0.5 * stirnflaeche * c_w * luftdichte * (v_ist ** 2)


def steigungswiderstand(alpha):
    return masse() * g * np.sin(alpha)


# Berechnung der zu überwindenden Fahrwiderstände
def fahrwiderstaende(v_ist, beschleunigung, steigung_in_prozent):
    alpha = np.arctan(steigung_in_prozent / 100)
    return rollwiderstand(alpha) + beschleunigungswiderstand(
        beschleunigung) + luftwiderstand(v_ist) + steigungswiderstand(alpha)
