# TODO: Umgang mit NaN-Werten, die auftreten, wenn in der Input-Routendatei z. B. keine Steigung angegeben ist für
#  bestimmte Stelle

import numpy as np
import pandas as pd
from Fahrzeugkomponenten import Fahrzeug, Nebenverbraucher, Batterie, Leistungselektronik, Elektromotor, Getriebe
import Fahrer
import Route

soc: float
route: np.ndarray
zeit_intervall = 1


def pause(nummer, laenge):
    liste = []
    global soc
    kumulierter_energieverbrauch = 0.0
    ladeleistung = 60000  # in Watt
    ladeleistung_batterie = Batterie.leistung(-ladeleistung)
    energieaufnahme = ladeleistung_batterie * zeit_intervall # in Joule

    for i in range(0, laenge):
        t = i
        kumulierter_energieverbrauch += energieaufnahme
        neue_zeile = {'Zeit [s]': t,
                  'SoC [%]': soc,
                  'Abgerufene Batterieleistung im Intervall [t, t+1) [W]': ladeleistung_batterie,
                  'Kumulierter Energieverbrauch nach Intervall [t, t+1) [J]': kumulierter_energieverbrauch}
        liste.append(neue_zeile)
        soc = Batterie.state_of_charge(energieaufnahme)

    pause_tabelle = pd.DataFrame(liste)
    with pd.ExcelWriter('Output.xlsx', mode='a') as writer:
        pause_tabelle.to_excel(writer, sheet_name='Pause Nr. ' + nummer, index=False)

    return pause_tabelle

def umlauf(nummer):
    # Der Batteriestand zu Beginn des Umlaufs wird festgelegt
    global soc, route
    streckenlaenge = route['distance_km'][len(route) - 1] * 1000  # in Metern

    # Initialisierung der Schleife
    t = 0  # Zeit in s
    v_ist = 0.0  # Ist-Geschwindigkeit in m/s
    zurueckgelegte_distanz = 0.0  # zurückgelegte Strecke in m
    kumulierter_energieverbrauch = 0.0
    liste = []

    # Schleife, die läuft bis Umlauf beendet
    # TODO: Halt an Bushaltestelle
    while zurueckgelegte_distanz < streckenlaenge:
        # TODO: Überlegen, was gehört zu t=0, was gehört zu t=1? Größen am Anfang/am Ende des betrachteten Intervalls

        # in Abhängigkeit der bereits zurückgelegten Distanz werden aktuelle Steigung sowie Soll-Geschwindigkeit aus der
        # Routendatei ermittelt
        steigung = Route.steigung(zurueckgelegte_distanz, route)
        v_soll = Route.v_soll(zurueckgelegte_distanz, route)

        # Der Fahrer wählt in Abhängigkeit von Soll- und Ist-Geschwindigkeit eine Beschleunigung oder Verzögerung aus
        beschleunigung = Fahrer.beschleunigung(v_ist, v_soll)

        # Ermittlung des Gesamtleistungsbedarfs
        fahrwiderstaende = Fahrzeug.fahrwiderstaende(v_ist, beschleunigung, steigung)

        benoetigte_leistung = Elektromotor.leistung(fahrwiderstaende, v_ist) + Nebenverbraucher.leistung
        leistung_batterie = Batterie.leistung(benoetigte_leistung)
        # Berechnung des Energieverbrauchs während des gewählten Zeitintervalls
        energieverbrauch_im_intervall = leistung_batterie * zeit_intervall # in Joule

        # Aktualisieren des Gesamtenergieverbrauchs im Umlauf
        kumulierter_energieverbrauch += energieverbrauch_im_intervall

        # Sammle neu gewonnene Daten in Liste
        neue_zeile = {'Zeit [s]': t,
                      'SoC [%]': soc,
                      'Zurückgelegte Distanz [m]': zurueckgelegte_distanz,
                      'Ist-Geschwindigkeit zum Zeitpunkt t [m/s]': v_ist,
                      'Soll-Geschwindigkeit zum Zeitpunkt t [m/s]': v_soll,
                      'Steigung im Intervall [t, t+1) [%]': steigung,
                      'Gewählte Beschleunigung im Intervall [t, t+1) [m/s²]': beschleunigung,
                      'Abgerufene Batterieleistung im Intervall [t, t+1) [W]': leistung_batterie,
                      'Kumulierter Energieverbrauch nach Intervall [t, t+1) [J]': kumulierter_energieverbrauch}
        liste.append(neue_zeile)

        # Laden bzw. Entladen der Batterie, Berechnung des neuen SoC
        soc = Batterie.state_of_charge(energieverbrauch_im_intervall)

        # Berechnung der zurückgelegten Strecke und der neuen Ist-Geschwindigkeit
        zurueckgelegte_distanz += 0.5 * beschleunigung * (zeit_intervall ** 2) + v_ist * zeit_intervall
        v_ist += beschleunigung * zeit_intervall
        t += zeit_intervall

    # Tabelle mit allen Daten des Umlaufs wird erstellt und zurückgegeben
    umlauf_tabelle = pd.DataFrame(liste)
    with pd.ExcelWriter('Output.xlsx', mode='a') as writer:
        umlauf_tabelle.to_excel(writer, sheet_name='Umlauf Nr. ' + nummer, index=False)

    return umlauf_tabelle