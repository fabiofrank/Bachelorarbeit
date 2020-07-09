inhalt = 0.0
kapazitaet = 0.0
effizienz = 0.0
effizienz_leistungselektronik = 0.0

# Der Energieverbrauch bzw. Energiegewinn wird berechnet unter Berücksichtigung von Batterieverlusten
def energieverbrauch(leistung, zeit_intervall):
    energie = leistung * zeit_intervall

    if energie < 0:
        delta = energie * (effizienz * effizienz_leistungselektronik)
    else:
        delta = energie / (effizienz * effizienz_leistungselektronik)
    return delta  # in Joule

# Die Batterie hat einen variablen Inhalt sowie eine feste Kapazität
# Der Batterieinhalt wird angepasst (Laden oder Entladen der Batterie)
# Der neue SoC wird zurückgegeben
def state_of_charge(delta):
    global inhalt
    inhalt -= delta / 3600000
    return inhalt / kapazitaet * 100  # SoC in Prozent
