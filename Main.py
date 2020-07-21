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
Betriebstag.route = Route.einlesen('20200715070018-25131-data.csv')

# Der SoC zu Beginn des Betriebstags wird festgelegt
Betriebstag.soc = 100.0
Batterie.inhalt = Batterie.kapazitaet * Betriebstag.soc / 100

# Es wird eingestellt, wie groß die Zeitschritte in der Simulation sein sollen
Betriebstag.zeit_intervall = 1 # in Sekunden

# TODO: Uhrzeit der einzelnen Umläufe?
# TODO: Übersicht über Betriebstag: Welche Werte sind interessant?

liste = []
# Aneinanderreihen von Umläufen
for i in range(1,4):
    print("Umlauf ", i, " gestartet.")
    soc_vor_umlauf = Betriebstag.soc
    aktueller_umlauf = Betriebstag.umlauf(nummer=str(i))
    ergebnis_umlauf = {'Umlauf bzw. Pause': 'Umlauf '+ str(i), 'SoC zu Beginn [%]': soc_vor_umlauf, 'SoC am Ende [%]': Betriebstag.soc, 'Energieverbrauch des Intervalls [kWh]': Betriebstag.kumulierter_energieverbrauch / 3600000}
    liste.append(ergebnis_umlauf)

    print('Pause ', i, ' gestartet.')
    soc_vor_pause = Betriebstag.soc
    aktuelle_pause = Betriebstag.pause(nummer=str(i), laenge=300)
    ergebnis_pause = {'Umlauf bzw. Pause': 'Pause '+ str(i), 'SoC zu Beginn [%]': soc_vor_pause, 'SoC am Ende [%]': Betriebstag.soc, 'Energieverbrauch des Intervalls [kWh]': Betriebstag.kumulierter_energieverbrauch / 3600000}
    liste.append(ergebnis_pause)

    print('--------------------------------')

print('Übersicht erstellen.')
uebersicht_betriebstag = pd.DataFrame(liste)
with pd.ExcelWriter('Output.xlsx', mode='a') as writer:
    uebersicht_betriebstag.to_excel(writer, sheet_name='Übersicht Betriebstag', index=False)