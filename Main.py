import datetime
import Betrieb
from Fahrzeugkomponenten import Fahrzeug, Batterie, Leistungselektronik, Elektromotor, Getriebe
import Route
import Output

#######################################################################################################################
# SCHRITT 1: FESTE PARAMETER DES SIMULIERTEN FAHRZEUGS FESTLEGEN

# siehe Dateien: 'Fahrzeug', 'Elektromotor', 'Batterie'

#######################################################################################################################
# SCHRITT 2: DIE PFADE DER INPUTDATEIEN ALS STRING ANGEBEN

hoehenprofil = '20200715070018-25131-data.csv'
strecke = 'Input.xlsx'

# Die Route des Umlaufs wird eingelesen
Route.hoehenprofil_einlesen(hoehenprofil)
Route.strecke_einlesen(strecke)

#######################################################################################################################

# SCHRITT 3: EINSTELLEN, WIE GROẞ DIE ZEITSCHRITTE IN DER SIMULATION SEIN SOLLEN
Betrieb.zeit_intervall = 1  # in Sekunden

# Uhrzeit des Betriebsstarts angeben
uhrzeit = '09:00'  # Format hh:mm
Betrieb.uhrzeit = datetime.datetime.strptime(uhrzeit, '%H:%M')

# TODO: Variable Passagieranzahl
# TODO: Keine Energieaufnahme, wenn SoC = 100 % !!!


# Aneinanderreihen von Umläufen
print("Pause")
Betrieb.pause(ende='09:30')
print("Umlauf")
Betrieb.umlauf(temperatur=20)
print('Pause')
Betrieb.pause(ende='11:00')
print('--------------------------------')

print('Übersicht erstellen.')

# Output als formatierte Tabelle in Excel-Dokument
Output.formatierung(Betrieb.daten_uebersicht, Betrieb.daten_umlaeufe)

