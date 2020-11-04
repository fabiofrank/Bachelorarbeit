import datetime
import Betrieb
import Route
import Ausgabe

#######################################################################################################################
# SCHRITT 1: NAME DER SIMULATION FESTLEGEN
name_simulation = 'Linie24_Test'

#######################################################################################################################
# SCHRITT 2: FESTE PARAMETER DES SIMULIERTEN FAHRZEUGS FESTLEGEN
# siehe Dateien: 'Fahrzeug', 'Elektromotor', 'Batterie', 'Nebenverbraucher', 'DWPT'

#######################################################################################################################
# SCHRITT 3: DIE STRECKENCHARAKTERISTIK DURCH AUSFÜLLEN EINER INPUTDATEI IN EXCEL FESTLEGEN
strecke = 'Inputdateien/Balingen Linie 24/Input_Basisszenario.xlsx'

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

hoehenprofil = 'Inputdateien/Balingen Linie 24/Hoehenprofil_Linie24.csv'

# Die Route des Umlaufs wird eingelesen
Route.hoehenprofil_einlesen(hoehenprofil)
Route.strecke_einlesen(strecke)

#######################################################################################################################
# SCHRITT 5: BETRIEBSSTART ANGEBEN (Programm stellt Uhrzeit ein)
uhrzeit_start = '07:18'  # Format hh:mm
Betrieb.uhrzeit = datetime.datetime.strptime(uhrzeit_start, '%H:%M')

#######################################################################################################################
# SCHRITT 6: UMLÄUFE UND LADEPAUSEN ANEINANDERREIHEN
# Befehle:
# Betrieb.umlauf(fahrgaeste, aussentemperatur)
# Betrieb.pause(ende=datetime.datetime.strptime('hh:mm')) mit Angabe, wann der nächste Umlauf beginnt

# Je nach Fahrplan können die Befehle mit Schleifen aneindergereiht werden.
# Außentemperaturen und Fahrgastzahlen können für jeden Umlauf neu festgelegt werden.

takt = 30 # 30-Minuten-Takt
uhrzeit_ende = '20:48'
mittagspause_start = '12:15'
mittagspause_ende = '12:45'
datetime_start = datetime.datetime.strptime(uhrzeit_start, '%H:%M')
datetime_ende = datetime.datetime.strptime(uhrzeit_ende, '%H:%M')
datetime_mittagspause_start = datetime.datetime.strptime(mittagspause_start, '%H:%M')
datetime_mittagspause_ende = datetime.datetime.strptime(mittagspause_ende, '%H:%M')

aussentemperatur = 20
fahrgaeste = 15

while Betrieb.uhrzeit < datetime_mittagspause_start:
    Betrieb.umlauf(fahrgaeste, aussentemperatur)
    datetime_start += datetime.timedelta(minutes=takt)
    Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)

Betrieb.pause(ende=datetime_mittagspause_ende, aussentemperatur=aussentemperatur)
datetime_start += datetime.timedelta(minutes=takt)
Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)

while Betrieb.uhrzeit < datetime_ende:
    Betrieb.umlauf(fahrgaeste, aussentemperatur)
    datetime_start += datetime.timedelta(minutes=takt)
    Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)

#######################################################################################################################
# FINALER SCHRITT: PROGRAMM AUSFÜHREN
# Die Outputdatei wird unter dem oben angegebenen Namen im Ordner Outputdateien gespeichert

#######################################################################################################################
# Output als formatierte Tabelle in Excel-Dokument
Ausgabe.formatierung(name_simulation, Betrieb.daten_uebersicht, Betrieb.daten_umlaeufe)

