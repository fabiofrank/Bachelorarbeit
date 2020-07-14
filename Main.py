import pandas as pd
import Betriebstag
from Fahrzeugkomponenten import Fahrzeug, Nebenverbraucher, Batterie, Leistungselektronik, Elektromotor, Getriebe
import Route

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
Betriebstag.route = Route.einlesen('Testdatensatz_10 Zeilen.csv')

# Der SoC zu Beginn des Betriebstags wird festgelegt
Betriebstag.soc = 100.0
Batterie.inhalt = Batterie.kapazitaet * Betriebstag.soc / 100

# Es wird eingestellt, wie groß die Zeitschritte in der Simulation sein sollen
Betriebstag.zeit_intervall = 1 # in Sekunden

# TODO: Uhrzeit der einzelnen Umläufe
# TODO: Übersicht über Betriebstag erstellen (Tabelle mit Umläufen): Dafür sind finale Werte der Umläufe nötig

# Aneinanderreihen von Umläufen
for i in range(1,3):
    print("Umlauf ", i, " gestartet.")
    aktueller_umlauf = Betriebstag.umlauf(nummer=str(i))
    print('Pause ', i, ' gestartet.')
    aktuelle_pause = Betriebstag.pause(nummer=str(i), laenge=3600)
    print('Zur Liste hinzufügen.')
