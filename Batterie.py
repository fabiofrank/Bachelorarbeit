
# Der Energieverbrauch bzw. Energiegewinn wird berechnet unter Berücksichtigung von Batterieverlusten
def energieverbrauch(leistung, zeit_intervall):
    energie = leistung * zeit_intervall
    effizienz_batterie = 0.95

    if energie < 0:
        delta = energie * effizienz_batterie
    else:
        delta = energie / effizienz_batterie
    return delta  # in Joule

# Die Batterie hat einen variablen Inhalt sowie eine feste Kapazität
# Der Batterieinhalt wird angepasst (Laden oder Entladen der Batterie)
# Der neue SoC wird zurückgegeben
def state_of_charge(delta):
    global inhalt
    global kapazitaet
    inhalt -= delta / 3600000
    return inhalt / kapazitaet * 100  # SoC in Prozent
