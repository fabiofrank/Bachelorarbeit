# TODO: zu Funktionen umschreiben

# Die Batterie hat den festen Parameter Kapazität und den variablen Inhalt

kapazitaet_kWh = 350  # in kWh
kapazitaet = kapazitaet_kWh * 3600000  # in Joule

inhalt_kWh = kapazitaet_kWh  # Initialisierung: Batterie ist voll
inhalt = inhalt_kWh * 3600000  # in Joule


def energieverbrauch(leistung, zeit_intervall):
    energie = leistung * zeit_intervall
    effizienz_batterie = 0.95

    if energie < 0:
        delta = energie * effizienz_batterie
    else:
        delta = energie / effizienz_batterie
    return delta  # in Joule


def state_of_charge(delta, inhalt):
    inhalt -= delta  # Update des Batterieinhalts in Joule
    return inhalt / kapazitaet * 100  # SoC in Prozent
