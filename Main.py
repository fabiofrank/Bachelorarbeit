import pandas as pd
import datetime
import Betrieb
from Fahrzeugkomponenten import Fahrzeug, Batterie, Leistungselektronik, Elektromotor, Getriebe
import Route
import Output

# TODO: feste Fahrzeugparameter auf Files verteilen oder ALLE hier platzieren
# SCHRITT 1: FESTE PARAMETER DES SIMULIERTEN FAHRZEUGS FESTLEGEN
Fahrzeug.masse_leer = 12760.0  # in kg
Fahrzeug.anzahl_fahrgaeste = 45 # Max. 90 Fahrgäste
Fahrzeug.stirnflaeche = 2.55 * 3.398  # in qm
Fahrzeug.f_roll = 0.015 # TODO: Quelle Rollwiderstandskoeffizient
Fahrzeug.c_w = 0.3 # TODO: Quelle cw-Wert
Fahrzeug.anzahl_spulen = 3
Batterie.kapazitaet = 345.6  # in KWh # TODO: Quelle Brutto-Netto-Umrechnung
Batterie.effizienz = 0.95 # TODO: Quelle Batterieverluste
Leistungselektronik.effizienz = 0.96 # TODO: Quelle LE-Wirkungsgrad
Elektromotor.effizienz = 0.95 # TODO: EM-Wirkungsgrad errechnen aus PRIMOVE-Daten
Elektromotor.maximale_leistung = 300000.0  # Watt # TODO: Quelle Max-Leistung EM
Getriebe.effizienz = 0.95 # TODO: Quelle Getriebeverluste

# SCHRITT 2: DIE PFADE DER INPUTDATEIEN ALS STRING ANGEBEN
hoehenprofil = '20200715070018-25131-data.csv'
strecke = 'Input.xlsx'

# Die Route des Umlaufs wird eingelesen
Route.hoehenprofil_einlesen(hoehenprofil)
Route.strecke_einlesen(strecke)

# Zu Beginn der Simulation ist Batterie vollgeladen
Batterie.inhalt = Batterie.kapazitaet

# Es wird eingestellt, wie groß die Zeitschritte in der Simulation sein sollen
Betrieb.zeit_intervall = 1  # in Sekunden

# Uhrzeit des Betriebsstarts angeben
uhrzeit = '09:00'  # Format hh:mm
Betrieb.uhrzeit = datetime.datetime.strptime(uhrzeit, '%H:%M')

# TODO: Ändert sich die Masse/Passagierzahl im Laufe des Betriebstags?
# TODO: Außentemperatur an Uhrzeit koppeln?
# TODO: Umlauf soll bei bestimmter Uhrzeit starten (Pausenlänge anpassen)

daten_uebersicht = []
daten_umlaeufe = []

# Aneinanderreihen von Umläufen
for i in range(1, 6):
    print("Umlauf ", i, " gestartet.")
    soc_vor_umlauf = Betrieb.soc
    uhrzeit_vor_umlauf = Betrieb.uhrzeit
    aktueller_umlauf = Betrieb.umlauf(temperatur=20)
    daten_umlaeufe.append(aktueller_umlauf)

    ergebnis_umlauf = {'Typ': 'Umlauf ' + str(i),
                       'Uhrzeit zu Beginn': datetime.datetime.strftime(uhrzeit_vor_umlauf, '%H:%M'),
                       'Uhrzeit am Ende': datetime.datetime.strftime(Betrieb.uhrzeit, '%H:%M'),
                       'Außentemperatur [°C]': Betrieb.aussentemperatur,
                       'SoC zu Beginn [%]': soc_vor_umlauf,
                       'SoC am Ende [%]': Betrieb.soc,
                       'Energieverbrauch des Intervalls [kWh]': Betrieb.kumulierter_energieverbrauch / 3600000}
    daten_uebersicht.append(ergebnis_umlauf)

    print('Pause ', i, ' gestartet.')
    soc_vor_pause = Betrieb.soc
    uhrzeit_vor_pause = Betrieb.uhrzeit
    aktuelle_pause = Betrieb.pause(laenge=300)
    daten_umlaeufe.append(aktuelle_pause)

    ergebnis_pause = {'Typ': 'Pause ' + str(i),
                      'Uhrzeit zu Beginn': datetime.datetime.strftime(uhrzeit_vor_pause, '%H:%M'),
                      'Uhrzeit am Ende': datetime.datetime.strftime(Betrieb.uhrzeit, '%H:%M'),
                      'Außentemperatur [°C]': Betrieb.aussentemperatur,
                      'SoC zu Beginn [%]': soc_vor_pause,
                      'SoC am Ende [%]': Betrieb.soc,
                      'Energieverbrauch des Intervalls [kWh]': Betrieb.kumulierter_energieverbrauch / 3600000}
    daten_uebersicht.append(ergebnis_pause)

    print('--------------------------------')

print('Übersicht erstellen.')

# Output als formatierte Tabelle in Excel-Dokument
Output.formatierung(daten_uebersicht, daten_umlaeufe)


