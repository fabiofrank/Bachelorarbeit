# TODO: Dokumente importieren
import Route, Fahrer, Fahrzeug
# TODO: Schleife, die den Energieverbrauch errechnet

# Initialisierung
t = 0 # Zeit in s
v_ist = 0 # Ist-Geschwindigkeit in m/s
distanz = 0 # zurückgelegte Strecke TODO: m oder km?
kumulierter_Energieverbrauch = 0

# Ein Objekt vom Typ Route wird mittels einer csv-Datei erzeugt
route = Route.Route("Testdatensatz_10 Zeilen.csv") # TODO: bessere Bezeichnungen überlegen bzw. abkürzen

# Ein Objekt vom Typ Antriebsstrang/Fahrzeug wird erzeugt und Parameter festgelegt
fahrzeug = Fahrzeug.Fahrzeug()
fahrzeug.masse = 12000
fahrzeug.stirnflaeche = 8.8




# in Abhängigkeit der bereits zurückgelegten Distanz werden aktuelle Steigung sowie Soll-Geschwindigkeit aus der Routendatei ermittelt
steigung = route.steigung(distanz)
v_soll = route.v_soll(distanz)

# Der Fahrer wählt in Abhängigkeit von Soll- und Ist-Geschwindigkeit eine Beschleunigung oder Verzögerung aus
beschleunigung = Fahrer.beschleunigung(v_ist, v_soll)

# Ermittlung der Leistung, die der Antriebsstrang benötigt
Fahrzeug.leistung()

