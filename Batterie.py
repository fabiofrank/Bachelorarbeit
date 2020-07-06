# TODO: zu Funktionen umschreiben
class Batterie:

    # Die Batterie hat den festen Parameter Kapazität und den variablen Inhalt

    kapazitaet_kWh = 350 # in kWh
    kapazitaet = kapazitaet_kWh * 3600000 # in Joule

    inhalt_kWh = kapazitaet_kWh # Initialisierung in kWh
    inhalt = inhalt_kWh * 3600000 # in Joule

    def energieverbrauch(self, leistung):
        zeit_intervall = 1 # in Sekunden
        energie = leistung * zeit_intervall
        effizienz_batterie = 0.95

        if energie < 0:
            delta = energie * effizienz_batterie
        else:
            delta = energie / effizienz_batterie

        return delta # in Joule

    def state_of_charge(self, delta):
        self.inhalt -= delta # Update des Batterieinhalts in Joule
        return self.inhalt / self.kapazitaet * 100 # SoC in Prozent

