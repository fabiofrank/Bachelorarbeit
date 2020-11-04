from Fahrzeugkomponenten import Leistungselektronik


#######################################################################################################################
# KONSTANTE PARAMETER, DIE FÜR DIE SIMULATION FESTGELEGT WERDEN MÜSSEN

# Nutzbare Kapazität der Batterie in kWh
kapazitaet = 174
# Effizienz der Batterie
effizienz = 0.9 # nach Absprache mit Markus Tesar 26.08.2020

# Effizienz der Leistungselektronik
Leistungselektronik.effizienz = 0.96 # nach Absprache mit Markus Tesar 26.08.2020

#######################################################################################################################


# Initialisierung: Zu Beginn ist die Batterie vollgeladen
inhalt = kapazitaet

# Die Entladeleistung (positiv) bzw. Ladeleistung (negativ) der Batterie wird berechnet
# Berücksichtigung von Verlusten in Batterie und Leistungselektronik
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
    inhalt -= (delta / 3600000)
    soc = inhalt / kapazitaet * 100
    return soc  # in %
