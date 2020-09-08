import datetime
import Betrieb
from Fahrzeugkomponenten import Fahrzeug, Batterie, Leistungselektronik, Elektromotor, Getriebe
import Route
import Ausgabe

#######################################################################################################################
# SCHRITT 1: NAME DER SIMULATION FESTLEGEN
name_simulation = 'Balingen_3Haltestellen_ohneDWPT'

#######################################################################################################################
# SCHRITT 2: FESTE PARAMETER DES SIMULIERTEN FAHRZEUGS FESTLEGEN

# siehe Dateien: 'Fahrzeug', 'Elektromotor', 'Batterie', 'Nebenverbraucher', 'DWPT'

#######################################################################################################################
# SCHRITT 3: DIE STRECKENCHARAKTERISTIK DURCH AUSFÜLLEN DER INPUTDATEI IN EXCEL FESTLEGEN

strecke = 'Inputdateien/Input_Balingen.xlsx'

#######################################################################################################################
# SCHRITT 4: MITHILFE VON GOOGLE MAPS UND GPS-VISUALIZER EINE CSV-DATEI MIT STEIGUNGSANGABEN GENERIEREN
#               1) Route in Google Maps konstruieren
#               2) https://www.gpsvisualizer.com/convert_input
#                   - Output format: plain text
#                   - URL aus Google Maps angeben
#                   - Google API-Key angeben
#                   - Plain text delimiter: comma
#                   - Add estimated fields: slope(%)
#                   - Add DEM elevation data: best available source
#               3) In angegebenem Pfad ablegen oder Pfad zur CSV-Datei hier angeben

hoehenprofil = 'Inputdateien/Hoehenprofil_Balingen.csv'

# Die Route des Umlaufs wird eingelesen
Route.hoehenprofil_einlesen(hoehenprofil)
Route.strecke_einlesen(strecke)

#######################################################################################################################
# SCHRITT 3: UHRZEIT DES BETRIEBSSTARTS ANGEBEN (hh:mm)

uhrzeit = '08:30'  # Format hh:mm
Betrieb.uhrzeit = datetime.datetime.strptime(uhrzeit, '%H:%M')

#######################################################################################################################
# SCHRITT 4: UMLÄUFE UND LADEPAUSEN ANEINANDERREIHEN
# Betrieb.umlauf(fahrgaeste, aussentemperatur)
# Betrieb.pause(ende='hh:mm') mit Angabe, wann die Ladepause beendet ist (und der nächste Umlauf beginnt)
Betrieb.pause(ende='09:00', aussentemperatur=20)
Betrieb.umlauf(fahrgaeste=90, aussentemperatur=20)

#######################################################################################################################

# Output als formatierte Tabelle in Excel-Dokument
Ausgabe.formatierung(name_simulation, Betrieb.daten_uebersicht, Betrieb.daten_umlaeufe)

