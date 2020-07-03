# TODO: Dokumente importieren
import Route, Fahrer, Fahrzeug, Batterie, Nebenverbraucher
# TODO: Schleife, die den Energieverbrauch errechnet

# Initialisierung
t = 0 # Zeit in s
v_ist = 0 # Ist-Geschwindigkeit in m/s
distanz = 0 # zurückgelegte Strecke TODO: m oder km?
kumulierter_Energieverbrauch = 0

# Ein Objekt vom Typ Route wird mittels einer csv-Datei erzeugt
route = Route.Route("Testdatensatz_10 Zeilen.csv") # TODO: bessere Bezeichnungen überlegen bzw. abkürzen

# Ein Objekt vom Typ Antriebsstrang/Fahrzeug wird erzeugt und Parameter festgelegt
# default-Werte: m=12000 kg, Stirnfläche=8.8m², f_roll = 0.015
fahrzeug = Fahrzeug.Fahrzeug() # TODO: bessere Bezeichnung
fahrzeug.masse = 12000.0
fahrzeug.stirnflaeche = 8.8

# Ein Objekt vom Typ Batterie wird erzeugt und die seine Parameter festgelegt
batterie = Batterie.Batterie() # TODO: bessere Bezeichnung
batterie.kapazitaet_kWh = 350.0 # in KWh
batterie.inhalt = 350.0 # initialer Batteriestand in kWh (default: 100% der Kapazität)

# in Abhängigkeit der bereits zurückgelegten Distanz werden aktuelle Steigung sowie Soll-Geschwindigkeit aus der Routendatei ermittelt
steigung = route.steigung(distanz)
v_soll = route.v_soll(distanz)

# Der Fahrer wählt in Abhängigkeit von Soll- und Ist-Geschwindigkeit eine Beschleunigung oder Verzögerung aus
beschleunigung = Fahrer.beschleunigung(v_ist, v_soll)

# Ermittlung des Gesamtleistungsbedarfs
leistung = fahrzeug.leistung(v_ist, beschleunigung, steigung) + Nebenverbraucher.leistung

# Berechnung des Energieverbrauchs während des gewählten Zeitintervalls, Entladen bzw. Aufladen der Batterie
aktueller_energieverbrauch = batterie.energieverbrauch(leistung)
neuer_soc = batterie.state_of_charge(aktueller_energieverbrauch)
kumulierter_Energieverbrauch += aktueller_energieverbrauch

print("EV:", kumulierter_Energieverbrauch)

