import Batterie
import Fahrer
import Fahrzeug
import Nebenverbraucher
import Route

# Ein Objekt vom Typ Route wird mittels einer csv-Datei erzeugt
route = Route.Route("Testdatensatz_10 Zeilen.csv")  # TODO: bessere Bezeichnungen überlegen bzw. abkürzen
zeit_intervall = 1  # in Sekunden

# Ein Objekt vom Typ Antriebsstrang/Fahrzeug wird erzeugt und Parameter festgelegt
# default-Werte: m=12000 kg, Stirnfläche=8.8m², f_roll = 0.015
fahrzeug = Fahrzeug.Fahrzeug()  # TODO: bessere Bezeichnung
fahrzeug.masse = 12000.0
fahrzeug.stirnflaeche = 8.8

# Ein Objekt vom Typ Batterie wird erzeugt und seine Parameter festgelegt
batterie = Batterie.Batterie()  # TODO: bessere Bezeichnung
batterie.kapazitaet_kWh = 350.0  # in KWh
batterie.inhalt_kWh = 350.0  # initialer Batteriestand in kWh (default: 100% der Kapazität)

# Initialisierung
t = 0  # Zeit in s
v_ist = 0.0  # Ist-Geschwindigkeit in m/s
distanz = 0.0  # zurückgelegte Strecke in km TODO: m oder km?
kumulierter_energieverbrauch_joule = 0.0

# Schleife, die läuft bis Umlauf beendet
for t in range(0, len(route.route)):
    # TODO: Überlegen, was gehört zu t=0, was gehört zu t=1
    print("Intervall t = [", t, ",", t + zeit_intervall, ")")
    # in Abhängigkeit der bereits zurückgelegten Distanz werden aktuelle Steigung sowie Soll-Geschwindigkeit aus der
    # Routendatei ermittelt
    steigung = route.steigung(distanz)
    print("Steigung: ", steigung, " %")
    v_soll = route.v_soll(distanz)
    print("Soll-Geschwindigkeit: ", v_soll, " m/s")

    # Der Fahrer wählt in Abhängigkeit von Soll- und Ist-Geschwindigkeit eine Beschleunigung oder Verzögerung aus
    beschleunigung = Fahrer.beschleunigung(v_ist, v_soll)
    print("Gewählte Beschleunigung: ", beschleunigung, " m/s²")

    # Ermittlung des Gesamtleistungsbedarfs
    leistung = fahrzeug.leistung(v_ist, beschleunigung, steigung) + Nebenverbraucher.leistung
    print("Gesamtleistungsbedarf: ", leistung, " Watt")

    # Berechnung des Energieverbrauchs während des gewählten Zeitintervalls, Entladen bzw. Aufladen der Batterie
    aktueller_energieverbrauch = batterie.energieverbrauch(leistung)
    print("Aktueller Energieverbrauch: ", aktueller_energieverbrauch, " Joule")
    neuer_soc = batterie.state_of_charge(aktueller_energieverbrauch)
    print("Neuer SoC: ", neuer_soc, " %")
    kumulierter_energieverbrauch_joule += aktueller_energieverbrauch
    kumulierter_energieverbrauch_kWh = kumulierter_energieverbrauch_joule / 3600000
    print("kumulierter Energieverbrauch: ", kumulierter_energieverbrauch_joule, "Joule / ",
          kumulierter_energieverbrauch_kWh, " kWh")

    # Berechnung der zurückgelegten Strecke und der neuen Ist-Geschwindigkeit
    distanz += 0.5 * beschleunigung * (zeit_intervall ** 2) + v_ist * zeit_intervall
    print("zurückgelegte Strecke: ", distanz, "m")
    v_ist += beschleunigung * zeit_intervall
    print("Ist-Geschwindigkeit: ", v_ist, " m/s / ", v_ist * 3.6, " km/h")

    print("___________________________________________________________________________")

    # TODO: Output-Array kreiieren anstatt print-Befehle
