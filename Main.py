import Betriebstag
from Fahrzeugkomponenten import Fahrzeug, Nebenverbraucher, Batterie, Leistungselektronik, Elektromotor, Getriebe
import Route

zeit_intervall = 1  # in Sekunden

# Die festen Fahrzeugparameter werden festgelegt
Fahrzeug.masse = 12000.0  # in kg
Fahrzeug.stirnflaeche = 8.8  # in qm
Fahrzeug.f_roll = 0.015
Fahrzeug.c_w = 0.3
Batterie.kapazitaet = 350.0  # in KWh
Batterie.effizienz = 0.95
Leistungselektronik.effizienz = 1.0
Elektromotor.effizienz = 0.9
Getriebe.effizienz = 1.0

# Die Route des Umlaufs wird eingelesen
# Der SoC zu Beginn des Betriebstags wird festgelegt
Betriebstag.route = Route.einlesen('Testdatensatz_10 Zeilen.csv')
Betriebstag.soc = 100.0


# Aneinanderreihen von Umläufen
# TODO: Ladepausen zwischen Umläufen
for i in range(1,5):
    Betriebstag.umlauf(nummer=str(i))
    # Betriebstag.pause...