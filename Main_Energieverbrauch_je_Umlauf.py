# TODO: Umgang mit NaN-Werten, die auftreten, wenn in der Input-Routendatei keine Steigung angegeben ist für
#  bestimmte Stelle

import numpy as np
import pandas as pd

from Fahrzeugkomponenten import Fahrzeug, Nebenverbraucher, Batterie, Leistungselektronik, Elektromotor, Getriebe
import Fahrer
import Route

# Die Route wird mittels CSV-Datei eingelesen
route = Route.einlesen('Testdatensatz_10 Zeilen.csv')
streckenlaenge = route['distance_km'][len(route) - 1] * 1000  # in Metern
zeit_intervall = 1  # in Sekunden

# Die festen Fahrzeugparameter werden festgelegt
Fahrzeug.masse = 12000.0  # in kg
Fahrzeug.stirnflaeche = 8.8  # in qm
Fahrzeug.f_roll = 0.015
Fahrzeug.c_w = 0.3
Batterie.kapazitaet = 350.0  # in KWh
Batterie.effizienz = 0.95
Leistungselektronik.effizienz = 1.0
Elektromotor.effizienz = 0.9
Getriebe.effizienz = 1.0

# Der Batteriestand zu Beginn des Umlaufs wird festgelegt
initialer_soc = 100  # in Prozent
Batterie.inhalt = Batterie.kapazitaet * initialer_soc / 100

# Initialisierung der Schleife
t = 0  # Zeit in s
v_ist = 0.0  # Ist-Geschwindigkeit in m/s
zurueckgelegte_distanz = 0.0  # zurückgelegte Strecke in m
kumulierter_energieverbrauch_joule = 0.0

# Erstellen der Datentabelle
spalten = np.array(
    ['Zeit [s]', 'SoC [%]', 'Zurückgelegte Distanz [m]', 'Ist-Geschwindigkeit zum Zeitpunkt t [m/s]',
     'Soll-Geschwindigkeit zum Zeitpunkt t [m/s]', 'Steigung im Intervall [t, t+1) [%]',
     'Gewählte Beschleunigung im Intervall [t, t+1) [m/s²]', 'Abgerufene Batterieleistung im Intervall [t, t+1) [W]',
     'Kumulierter Energieverbrauch nach Intervall [t, t+1) [kWh]'])
umlauf_array = pd.DataFrame(columns=spalten)

# Schleife, die läuft bis Umlauf beendet
while zurueckgelegte_distanz < streckenlaenge:
    # TODO: Überlegen, was gehört zu t=0, was gehört zu t=1? Größen am Anfang/am Ende des betrachteten Intervalls

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
    fahrwiderstaende = Fahrzeug.fahrwiderstaende(v_ist, beschleunigung, steigung)
    benoetigte_leistung = Elektromotor.leistung(fahrwiderstaende, v_ist) + Nebenverbraucher.leistung
    leistung_batterie = Batterie.leistung(benoetigte_leistung)
    print("Momentane Leistung an der Batterie: ", leistung_batterie, " Watt")

    # Berechnung des Energieverbrauchs während des gewählten Zeitintervalls, Entladen bzw. Aufladen der Batterie
    energieverbrauch_im_intervall = leistung_batterie * zeit_intervall
    neuer_soc = Batterie.state_of_charge(energieverbrauch_im_intervall)
    print("Neuer SoC: ", neuer_soc, " %")

    # Aktualisieren des Gesamtenergieverbrauchs im Umlauf
    kumulierter_energieverbrauch_joule += energieverbrauch_im_intervall
    kumulierter_energieverbrauch_kWh = kumulierter_energieverbrauch_joule / 3600000
    print("Kumulierter Energieverbrauch: ", kumulierter_energieverbrauch_joule, "Joule / ",
          kumulierter_energieverbrauch_kWh, " kWh")

    # Füge neu gewonnene Daten zum Array hinzu
    neue_zeile = {'Zeit [s]': t, 'SoC [%]': neuer_soc,
                  'Zurückgelegte Distanz [m]': zurueckgelegte_distanz, 'Ist-Geschwindigkeit zum Zeitpunkt t [m/s]': v_ist,
                  'Soll-Geschwindigkeit zum Zeitpunkt t [m/s]': v_soll, 'Steigung im Intervall [t, t+1) [%]': steigung,
                  'Gewählte Beschleunigung im Intervall [t, t+1) [m/s²]': beschleunigung,
                  'Abgerufene Batterieleistung im Intervall [t, t+1) [W]': leistung_batterie,
                  'Kumulierter Energieverbrauch nach Intervall [t, t+1) [kWh]': kumulierter_energieverbrauch_kWh}
    umlauf_array = umlauf_array.append(neue_zeile, ignore_index=True)

    # Berechnung der zurückgelegten Strecke und der neuen Ist-Geschwindigkeit
    zurueckgelegte_distanz += 0.5 * beschleunigung * (zeit_intervall ** 2) + v_ist * zeit_intervall
    print("Zurückgelegte Strecke: ", zurueckgelegte_distanz, "m")
    v_ist += beschleunigung * zeit_intervall
    print("Ist-Geschwindigkeit: ", v_ist, " m/s / ", v_ist * 3.6, " km/h")
    t += zeit_intervall

    print("_________________________________________________________________________________________")

print(umlauf_array)
umlauf_array.to_excel('Output.xlsx')
