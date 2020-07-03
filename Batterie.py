# TODO: zu Funktionen umschreiben
class Batterie:
    kapazitaet_kWh = 350 # in kWh
    kapazitaet = kapazitaet_kWh * 3600000
    inhalt = kapazitaet # Initialisierung

    def energieverbrauch(self, leistung):
        zeit_intervall = 1 # in Sekunden
        energie = leistung * zeit_intervall
        effizienz_batterie = 0.95

        if energie < 0:
            delta = energie * effizienz_batterie
        else:
            delta = energie / effizienz_batterie

        return delta / 3600000 # Umrechnung von Joule in kWh

    def state_of_charge(self, delta):
        self.inhalt -= delta # Update des Batterieinhalts TODO: hier oder lieber in energieverbrauch()?
        soc = self.inhalt / self.kapazitaet

