import datetime
import Betrieb
from Fahrzeugkomponenten import Fahrzeug, Batterie, Leistungselektronik, Elektromotor, Getriebe
import Route
import Ausgabe

# TODO: Name der Simulation
#######################################################################################################################
# SCHRITT 1: FESTE PARAMETER DES SIMULIERTEN FAHRZEUGS FESTLEGEN

# siehe Dateien: 'Fahrzeug', 'Elektromotor', 'Batterie', 'Nebenverbraucher', 'DWPT'

#######################################################################################################################
# NAME DER SIMULATION FESTLEGEN (ALS STRING)
name_simulation = 'Testsimulation'

#######################################################################################################################
# SCHRITT 2: DIE PFADE DER INPUTDATEIEN ALS STRING ANGEBEN

hoehenprofil = 'Inputdateien/20200715070018-25131-data.csv'
strecke = 'Inputdateien/Input.xlsx'

# Die Route des Umlaufs wird eingelesen
Route.hoehenprofil_einlesen(hoehenprofil)
Route.strecke_einlesen(strecke)

#######################################################################################################################
# SCHRITT 3: UHRZEIT DES BETRIEBSSTARTS ANGEBEN (hh:mm)

uhrzeit = '09:00'  # Format hh:mm
Betrieb.uhrzeit = datetime.datetime.strptime(uhrzeit, '%H:%M')

#######################################################################################################################
# SCHRITT 4: UMLÄUFE UND LADEPAUSEN ANEINANDERREIHEN
# Betrieb.umlauf()
# Betrieb.pause(ende='hh:mm') mit Angabe, wann die Ladepause beendet ist

# TODO: Fahrplan umsetzen
Betrieb.pause(ende='09:30')
Betrieb.umlauf()
Betrieb.pause(ende='11:00')

#######################################################################################################################

# Output als formatierte Tabelle in Excel-Dokument
Ausgabe.formatierung(name_simulation, Betrieb.daten_uebersicht, Betrieb.daten_umlaeufe)

