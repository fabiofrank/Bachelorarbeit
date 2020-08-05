from typing import Any, Union

import numpy as np
import pandas as pd
from Fahrzeugkomponenten import Fahrzeug, Nebenverbraucher, Batterie, Leistungselektronik, Elektromotor, Getriebe
import Fahrer
import Route

soc: float
# route: pd.DataFrame
kumulierter_energieverbrauch: float
zeit_intervall = 1


def pause(nummer, laenge):
    liste = []
    global soc, kumulierter_energieverbrauch
    kumulierter_energieverbrauch = 0.0  # in Joule
    ladeleistung = 60000  # in Watt
    ladeleistung_batterie = Batterie.leistung(-ladeleistung)
    energieaufnahme = ladeleistung_batterie * zeit_intervall  # in Joule

    for i in range(0, laenge):
        t = i
        kumulierter_energieverbrauch += energieaufnahme
        neue_zeile = {'Typ': 'Pause',
                      'Zeit [s]': t,
                      'SoC [%]': soc,
                      'Abgerufene Batterieleistung im Intervall [t, t+1) [kW]': ladeleistung_batterie / 1000,
                      'Kumulierter Energieverbrauch nach Intervall [t, t+1) [KWh]': kumulierter_energieverbrauch / 3600000}
        liste.append(neue_zeile)
        soc = Batterie.state_of_charge(energieaufnahme)

    pause_tabelle = pd.DataFrame(liste)
    return pause_tabelle


def umlauf(nummer):
    global soc, kumulierter_energieverbrauch
    streckenlaenge = Route.route['distance (km)'].iloc[-1] * 1000  # in m

    # Initialisierung der Schleife
    t = 0  # Zeit in s
    v_ist = 0.0  # Ist-Geschwindigkeit in m/s
    zurueckgelegte_distanz = 0.0  # zurückgelegte Strecke in m
    kumulierter_energieverbrauch = 0.0
    liste = []

    # Schleife, die läuft bis Umlauf beendet
    # TODO: Halt an Bushaltestelle
    while zurueckgelegte_distanz < streckenlaenge:
        # in Abhängigkeit der bereits zurückgelegten Distanz werden aktuelle Steigung sowie Soll-Geschwindigkeit aus der
        # Routendatei ermittelt
        steigung = Route.steigung(zurueckgelegte_distanz)
        v_soll = Route.v_soll(zurueckgelegte_distanz)
        ladeleistung = Route.dwpt_ladeleistung(zurueckgelegte_distanz)

        # Der Fahrer wählt in Abhängigkeit von Soll- und Ist-Geschwindigkeit eine Beschleunigung oder Verzögerung aus
        beschleunigung = Fahrer.beschleunigung(v_ist, v_soll)

        # Ermittlung des Gesamtleistungsbedarfs
        fahrwiderstaende = Fahrzeug.fahrwiderstaende(v_ist, beschleunigung, steigung)

        benoetigte_leistung = Elektromotor.leistung(fahrwiderstaende, v_ist) + Nebenverbraucher.leistung - ladeleistung
        leistung_batterie = Batterie.leistung(benoetigte_leistung)
        # Berechnung des Energieverbrauchs während des gewählten Zeitintervalls
        energieverbrauch_im_intervall = leistung_batterie * zeit_intervall  # in Joule

        # Aktualisieren des Gesamtenergieverbrauchs im Umlauf
        kumulierter_energieverbrauch += energieverbrauch_im_intervall

        # Sammle neu gewonnene Daten in Liste
        neue_zeile = {'Typ': 'Umlauf',
                      'Zeit \n[s]': t,
                      'SoC \n[%]': soc,
                      'Zurückgelegte Distanz \n[m]': zurueckgelegte_distanz,
                      'Ist-Geschwindigkeit zum Zeitpunkt t \n[km/h]': v_ist * 3.6,
                      'Soll-Geschwindigkeit zum Zeitpunkt t \n[km/h]': v_soll * 3.6,
                      'Steigung im Intervall [t, t+1) \n[%]': steigung,
                      'Gewählte Beschleunigung im Intervall [t, t+1) \n[m/s²]': beschleunigung,
                      'Empfangene Leistung mittels DWPT \n[kW]': ladeleistung / 1000,
                      'Abgerufene Batterieleistung im Intervall [t, t+1) \n[kW]': leistung_batterie / 1000,
                      'Kumulierter Energieverbrauch nach Intervall [t, t+1) \n[kWh]': kumulierter_energieverbrauch / 3600000}
        liste.append(neue_zeile)

        # Laden bzw. Entladen der Batterie, Berechnung des neuen SoC
        soc = Batterie.state_of_charge(energieverbrauch_im_intervall)

        # Berechnung der zurückgelegten Strecke und der neuen Ist-Geschwindigkeit
        zurueckgelegte_distanz += 0.5 * beschleunigung * (zeit_intervall ** 2) + v_ist * zeit_intervall
        v_ist += beschleunigung * zeit_intervall
        t += zeit_intervall

    # Tabelle mit allen relevanten Daten des Umlaufs wird erstellt und zurückgegeben
    umlauf_tabelle = pd.DataFrame(liste)
    return umlauf_tabelle
