import numpy as np
from scipy import constants
import Fahrer

# TODO: Antriebsstrang als Klasse schreiben?

# physikalische Konstanten
g = constants.g
luftdichte = 1.225  # in kg/m³

class Fahrzeug:

    # feste Parameter TODO: diese als Tabelle eingeben?
    masse = 12000  # in kg
    f_roll = 0.015  # Rollwiderstandbeiwert [ohne Einheit]
    stirnflaeche = 8.8
    c_w = 0.3  # Luftwiderstandsbeiwert

    # dynamischer Input: Ist-Geschwindigkeit in m/s, gewählte Beschleunigung in m/s² aus Fahrermodell
    v_ist = Fahrer.v_ist
    beschleunigung = Fahrer.gewaehlte_beschleunigung
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


    def leistung():
        # Berechnung der zu überwindenden Fahrwiderstände
        fahrwiderstaende = rollwiderstand() + beschleunigungswiderstand() + luftwiderstand() + steigungswiderstand()

        # Berechnung der Leistung, die der Antriebsstrang benötigt bzw. abgibt unter Berücksichtigung von Verlusten
        effizienz_antriebsstrang = 0.9 # Motor, Getriebe, ...

        if fahrwiderstaende < 0:
            leistung = fahrwiderstaende * v_ist * effizienz_antriebsstrang
        else:
            leistung = (fahrwiderstaende * v_ist) / effizienz_antriebsstrang

        print("Leistung: ", leistung)
        return leistung