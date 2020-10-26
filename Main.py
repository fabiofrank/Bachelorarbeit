import datetime
import Betrieb
import Route
import Ausgabe

#######################################################################################################################
# SCHRITT 1: NAME DER SIMULATION FESTLEGEN
name_simulation = 'RDK_Shuttle'

#######################################################################################################################
# SCHRITT 2: FESTE PARAMETER DES SIMULIERTEN FAHRZEUGS FESTLEGEN

# siehe Dateien: 'Fahrzeug', 'Elektromotor', 'Batterie', 'Nebenverbraucher', 'DWPT'

#######################################################################################################################
# SCHRITT 3: DIE STRECKENCHARAKTERISTIK DURCH AUSFÜLLEN DER INPUTDATEI IN EXCEL FESTLEGEN

strecke = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Inputdateien\Input_Karlsruhe_großeRunde.xlsx'

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

hoehenprofil = 'Inputdateien/Hoehenprofil_KA.csv'

# Die Route des Umlaufs wird eingelesen
Route.hoehenprofil_einlesen(hoehenprofil)
Route.strecke_einlesen(strecke)

#######################################################################################################################
# SCHRITT 3: BETRIEBSSTART UND -ENDE ANGEBEN (hh:mm) SOWIE DEN TAKT (min)

uhrzeit_start = '06:00'  # Format hh:mm
uhrzeit_ende = '20:48'
mittagspause_start = '12:15'
mittagspause_ende = '12:45'
takt = 30 # 30-Minuten-Takt

Betrieb.uhrzeit = datetime.datetime.strptime(uhrzeit_start, '%H:%M')
datetime_start = datetime.datetime.strptime(uhrzeit_start, '%H:%M')
datetime_ende = datetime.datetime.strptime(uhrzeit_ende, '%H:%M')
datetime_mittagspause_start = datetime.datetime.strptime(mittagspause_start, '%H:%M')
datetime_mittagspause_ende = datetime.datetime.strptime(mittagspause_ende, '%H:%M')

#######################################################################################################################
# SCHRITT 4: UMLÄUFE UND LADEPAUSEN ANEINANDERREIHEN
# Betrieb.umlauf(fahrgaeste, aussentemperatur)
# Betrieb.pause(ende='hh:mm') mit Angabe, wann die Ladepause beendet ist (und der nächste Umlauf beginnt)

aussentemperatur = 35
fahrgaeste = 30

Betrieb.umlauf(fahrgaeste, aussentemperatur)

strecke = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Inputdateien\Input_Karlsruhe_kleineRunde.xlsx'
Betrieb.pause(datetime.datetime.strptime('07:06', '%H:%M'), 35)
Betrieb.umlauf(fahrgaeste, aussentemperatur)
Betrieb.pause(datetime.datetime.strptime('07:33', '%H:%M'), 35)
Betrieb.umlauf(fahrgaeste, aussentemperatur)
Betrieb.pause(datetime.datetime.strptime('08:06', '%H:%M'), 35)
Betrieb.umlauf(fahrgaeste, aussentemperatur)

strecke = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Inputdateien\Input_Karlsruhe_großeRunde.xlsx'
Betrieb.pause(datetime.datetime.strptime('12:30', '%H:%M'), 35)
Betrieb.umlauf(fahrgaeste, aussentemperatur)
Betrieb.pause(datetime.datetime.strptime('15:45', '%H:%M'), 35)
Betrieb.umlauf(fahrgaeste, aussentemperatur)

strecke = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Inputdateien\Input_Karlsruhe_kleineRunde.xlsx'
Betrieb.pause(datetime.datetime.strptime('16:50', '%H:%M'), 35)
Betrieb.umlauf(fahrgaeste, aussentemperatur)
Betrieb.pause(datetime.datetime.strptime('17:20', '%H:%M'), 35)
Betrieb.umlauf(fahrgaeste, aussentemperatur)

# while Betrieb.uhrzeit < datetime_ende:
#     Betrieb.umlauf(fahrgaeste, aussentemperatur)
#     datetime_start += datetime.timedelta(minutes=takt)
#     Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)


# #----------------------------------------------------------------------------
#fahrgaeste_NVZ = 15
#fahrgaeste_HVZ = 45

# while Betrieb.uhrzeit < datetime.datetime.strptime('09:00', '%H:%M'):
#     Betrieb.umlauf(fahrgaeste_HVZ, aussentemperatur)
#     datetime_start += datetime.timedelta(minutes=takt)
#     Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)
#
# #strecke = 'Inputdateien/Input_Basisszenario.xlsx'
# #Route.strecke_einlesen(strecke)
# while Betrieb.uhrzeit < datetime.datetime.strptime('11:30', '%H:%M'):
#     Betrieb.umlauf(fahrgaeste_NVZ, aussentemperatur)
#     datetime_start += datetime.timedelta(minutes=takt)
#     Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)
#
# #strecke = 'Inputdateien/Input_HVZ.xlsx'
# #Route.strecke_einlesen(strecke)
# while Betrieb.uhrzeit < datetime_mittagspause_start:
#     Betrieb.umlauf(fahrgaeste_HVZ, aussentemperatur)
#     datetime_start += datetime.timedelta(minutes=takt)
#     Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)
#
# Betrieb.pause(ende=datetime_mittagspause_ende, aussentemperatur=aussentemperatur)
# datetime_start += datetime.timedelta(minutes=takt)
# Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)
#
# while Betrieb.uhrzeit < datetime.datetime.strptime('13:30', '%H:%M'):
#     Betrieb.umlauf(fahrgaeste_HVZ, aussentemperatur)
#     datetime_start += datetime.timedelta(minutes=takt)
#     Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)
#
# #strecke = 'Inputdateien/Input_Basisszenario.xlsx'
# #Route.strecke_einlesen(strecke)
# while Betrieb.uhrzeit < datetime.datetime.strptime('15:30', '%H:%M'):
#     Betrieb.umlauf(fahrgaeste_NVZ, aussentemperatur)
#     datetime_start += datetime.timedelta(minutes=takt)
#     Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)
#
# #strecke = 'Inputdateien/Input_HVZ.xlsx'
# #Route.strecke_einlesen(strecke)
# while Betrieb.uhrzeit < datetime.datetime.strptime('17:30', '%H:%M'):
#     Betrieb.umlauf(fahrgaeste_HVZ, aussentemperatur)
#     datetime_start += datetime.timedelta(minutes=takt)
#     Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)
#
# #strecke = 'Inputdateien/Input_Basisszenario.xlsx'
# #Route.strecke_einlesen(strecke)
# while Betrieb.uhrzeit < datetime_ende:
#     Betrieb.umlauf(fahrgaeste_NVZ, aussentemperatur)
#     datetime_start += datetime.timedelta(minutes=takt)
#     Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)

########################################################################################
# while Betrieb.uhrzeit < datetime_mittagspause_start:
#     Betrieb.umlauf(fahrgaeste, aussentemperatur)
#     datetime_start += datetime.timedelta(minutes=takt)
#     Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)
#
# Betrieb.pause(ende=datetime_mittagspause_ende, aussentemperatur=aussentemperatur)
# datetime_start += datetime.timedelta(minutes=takt)
# Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)
#
# while Betrieb.uhrzeit < datetime_ende:
#     Betrieb.umlauf(fahrgaeste, aussentemperatur)
#     datetime_start += datetime.timedelta(minutes=takt)
#     Betrieb.pause(ende=datetime_start, aussentemperatur=aussentemperatur)
#######################################################################################################################

# Output als formatierte Tabelle in Excel-Dokument
Ausgabe.formatierung(name_simulation, Betrieb.daten_uebersicht, Betrieb.daten_umlaeufe)

