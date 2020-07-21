import math
from Fahrzeugkomponenten import Leistungselektronik

inhalt: float
kapazitaet: float
effizienz: float


# Der Energieverbrauch bzw. Energiegewinn wird berechnet
# unter Berücksichtigung von Verlusten in Batterie und Leistungselektronik
def leistung(benoetigte_leistung):
    if benoetigte_leistung < 0:
        leistung_batterie = benoetigte_leistung * (effizienz * Leistungselektronik.effizienz)
    else:
        leistung_batterie = benoetigte_leistung / (effizienz * Leistungselektronik.effizienz)
    return leistung_batterie  # in Watt


# Die Batterie hat einen variablen Inhalt sowie eine feste Kapazität
# Der Batterieinhalt wird angepasst (Laden oder Entladen der Batterie)
# Der neue SoC wird zurückgegeben
# SoC kann nicht über 100% sein
def state_of_charge(delta):
    global inhalt
    neuer_inhalt = inhalt - (delta / 3600000)
    if neuer_inhalt >= kapazitaet:
        soc = 100.0
    else:
        inhalt = neuer_inhalt
        soc = inhalt / kapazitaet * 100
    return soc  # in %
