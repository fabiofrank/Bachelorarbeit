# TODO: Umgang mit NaN
# TODO: mit globalen Variablen arbeiten anstelle von Argumenten, die an Funktionen weitergegeben werden

import Batterie
import Fahrer
import Fahrzeug
import Nebenverbraucher
import Route

# Die Route wird mittels CSV-Datei eingelesen
route = Route.einlesen('Testdatensatz_10 Zeilen.csv')
streckenlaenge = route['distance_km'][len(route) - 1] * 1000  # in Metern
zeit_intervall = 1  # in Sekunden

# Ein Objekt vom Typ Antriebsstrang/Fahrzeug wird erzeugt und Parameter festgelegt
# default-Werte: m=12000 kg, Stirnfläche=8.8m², f_roll = 0.015
Fahrzeug.masse = 12000.0
Fahrzeug.stirnflaeche = 8.8
Fahrzeug.f_roll = 0.015
Fahrzeug.c_w = 0.3

# Batterie wird parametrisiert
Batterie.kapazitaet = 350.0  # in KWh
Batterie.inhalt = 350.0  # Batteriestand zu Beginn des Umlaufs in kWh

# Initialisierung
t = 0  # Zeit in s
v_ist = 0.0  # Ist-Geschwindigkeit in m/s
zurueckgelegte_distanz = 0.0  # zurückgelegte Strecke in km TODO: m oder km?
kumulierter_energieverbrauch_joule = 0.0

# Schleife, die läuft bis Umlauf beendet
while zurueckgelegte_distanz < streckenlaenge:
    # TODO: Überlegen, was gehört zu t=0, was gehört zu t=1
    print("Intervall t = [", t, ",", t + zeit_intervall, ")")

    # in Abhängigkeit der bereits zurückgelegten Distanz werden aktuelle Steigung sowie Soll-Geschwindigkeit aus der
    # Routendatei ermittelt
    steigung = Route.steigung(zurueckgelegte_distanz, route)
    print("Steigung: ", steigung, " %")
    v_soll = Route.v_soll(zurueckgelegte_distanz, route)
    print("Soll-Geschwindigkeit: ", v_soll, " m/s")

    # Der Fahrer wählt in Abhängigkeit von Soll- und Ist-Geschwindigkeit eine Beschleunigung oder Verzögerung aus
    beschleunigung = Fahrer.beschleunigung(v_ist, v_soll)
    print("Gewählte Beschleunigung: ", beschleunigung, " m/s²")

    # Ermittlung des Gesamtleistungsbedarfs
    # TODO: Austauschen durch Leistung an der Batterie
    leistung = Fahrzeug.leistung(v_ist, beschleunigung, steigung) + Nebenverbraucher.leistung
    print("Gesamtleistungsbedarf: ", leistung, " Watt")

    # Berechnung des Energieverbrauchs während des gewählten Zeitintervalls, Entladen bzw. Aufladen der Batterie
    energieverbrauch_im_intervall = Batterie.energieverbrauch(leistung, zeit_intervall)
    print("Aktueller Energieverbrauch: ", energieverbrauch_im_intervall, " Joule")
    neuer_soc = Batterie.state_of_charge(energieverbrauch_im_intervall)
    print("Neuer SoC: ", neuer_soc, " %")
    kumulierter_energieverbrauch_joule += energieverbrauch_im_intervall
    kumulierter_energieverbrauch_kWh = kumulierter_energieverbrauch_joule / 3600000
    print("Kumulierter Energieverbrauch: ", kumulierter_energieverbrauch_joule, "Joule / ",
          kumulierter_energieverbrauch_kWh, " kWh")

    # Berechnung der zurückgelegten Strecke und der neuen Ist-Geschwindigkeit
    zurueckgelegte_distanz += 0.5 * beschleunigung * (zeit_intervall ** 2) + v_ist * zeit_intervall
    print("Zurückgelegte Strecke: ", zurueckgelegte_distanz, "m")
    v_ist += beschleunigung * zeit_intervall
    print("Ist-Geschwindigkeit: ", v_ist, " m/s / ", v_ist * 3.6, " km/h")
    t += zeit_intervall

    print("_________________________________________________________________________________________")

    # TODO: Output-Array kreiieren anstatt print-Befehle
