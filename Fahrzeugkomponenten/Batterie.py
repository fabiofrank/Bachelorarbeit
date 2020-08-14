from Fahrzeugkomponenten import Leistungselektronik


#######################################################################################################################
# KONSTANTE PARAMETER, DIE FÜR DIE SIMULATION FESTGELEGT WERDEN MÜSSEN

# Nutzbare Kapazität der Batterie in kWh
kapazitaet = 345.6 * 0.8 # TODO: Quelle Brutto-Netto-Umrechnung

# Effizienz der Batterie
effizienz = 0.95 # TODO: Quelle

# Effizienz der Leistungselektronik
Leistungselektronik.effizienz = 0.96 # TODO: Quelle

#######################################################################################################################


# Initialisierung: Zu Beginn ist die Batterie vollgeladen
inhalt = kapazitaet

# Die Entladeleistung (positiv) bzw. Ladeleistung (negativ) der Batterie wird berechnet
# erücksichtigung von Verlusten in Batterie und Leistungselektronik
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
