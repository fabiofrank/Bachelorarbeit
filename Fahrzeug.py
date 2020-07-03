import numpy as np
from scipy import constants

# TODO: Fahrzeug als Klasse, Antriebsstrang (evtl. Batterie) als subclass?

# physikalische Konstanten
g = constants.g
luftdichte = 1.225  # in kg/m³


class Fahrzeug:
    # feste Parameter TODO: diese als Tabelle eingeben?
    masse = 12000.0  # in kg
    f_roll = 0.015  # Rollwiderstandbeiwert [ohne Einheit]
    stirnflaeche = 8.8
    c_w = 0.3  # Luftwiderstandsbeiwert

    # Formeln der auftretenden Fahrwiderstände
    def rollwiderstand(self, alpha):
        return self.masse * g * np.cos(alpha) * self.f_roll

    def beschleunigungswiderstand(self, beschleunigung):
        return self.masse * beschleunigung

    def luftwiderstand(self, v_ist):
        return 0.5 * self.stirnflaeche * self.c_w * luftdichte * (v_ist ** 2)

    def steigungswiderstand(self, alpha):
        return self.masse * g * np.sin(alpha)

    def leistung(self, v_ist, beschleunigung, steigung_in_prozent):
        alpha = np.arctan(steigung_in_prozent / 100)

        # Berechnung der zu überwindenden Fahrwiderstände
        fahrwiderstaende = self.rollwiderstand(alpha) + self.beschleunigungswiderstand(
            beschleunigung) + self.luftwiderstand(v_ist) + self.steigungswiderstand(alpha)

        # Berechnung der Leistung, die der Antriebsstrang benötigt bzw. abgibt unter Berücksichtigung von Verlusten
        effizienz_antriebsstrang = 0.9  # Motor, Getriebe, ...
        if fahrwiderstaende < 0:
            leistung = fahrwiderstaende * v_ist * effizienz_antriebsstrang
        else:
            leistung = (fahrwiderstaende * v_ist) / effizienz_antriebsstrang

        return leistung
