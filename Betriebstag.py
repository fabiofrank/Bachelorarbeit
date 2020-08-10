import datetime
import pandas as pd

import Fahrer
import Route
from Fahrzeugkomponenten import Fahrzeug, Nebenverbraucher, Batterie, Elektromotor

soc: float
uhrzeit: datetime
aussentemperatur: float
kumulierter_energieverbrauch: float
zeit_intervall = 1
t: int
zurueckgelegte_distanz: float
v_ist: float
v_soll: float
steigung: float
beschleunigung: float
ladeleistung: float
leistung_batterie: float
liste: list
energieverbrauch_im_intervall: float


def pause(laenge):
    global soc, kumulierter_energieverbrauch, uhrzeit, t, liste, ladeleistung
    liste = []
    kumulierter_energieverbrauch = 0.0  # in Joule
    wirkungsgrad_induktiv = 0.9
    ladeleistung_spule = 25000  # in Watt
    ladeleistung = Fahrzeug.anzahl_spulen * ladeleistung_spule * wirkungsgrad_induktiv  # in Watt
    ladeleistung_batterie = Batterie.leistung(-ladeleistung)
    energieaufnahme = ladeleistung_batterie * zeit_intervall  # in Joule

    for i in range(0, laenge):
        t = i
        kumulierter_energieverbrauch += energieaufnahme
        neue_zeile = {'Uhrzeit': datetime.datetime.strftime(uhrzeit, '%H:%M:%S'),
                      'Typ': 'Pause',
                      'Zeit [s]': t,
                      'SoC [%]': soc,
                      'Abgerufene Batterieleistung im Intervall [t, t+1) [kW]': ladeleistung_batterie / 1000,
                      'Kumulierter Energieverbrauch nach Intervall [t, t+1) [KWh]': kumulierter_energieverbrauch
                                                                                    / 3600000}
        liste.append(neue_zeile)
        soc = Batterie.state_of_charge(energieaufnahme)
        uhrzeit += datetime.timedelta(seconds=zeit_intervall)

    pause_tabelle = pd.DataFrame(liste)
    return pause_tabelle


def anhalten(geschwindigkeit, verzoegerung):
    global t
    # Errechnen wie lange Bremsung mit gegebener Verzögerung von v_ist auf 0 dauert
    bremszeit = round(geschwindigkeit / verzoegerung)  # in ganzen Sekunden
    return bremszeit


def umlauf(temperatur):
    global soc, kumulierter_energieverbrauch, uhrzeit, t, zurueckgelegte_distanz, v_ist, v_soll, steigung,\
        beschleunigung, leistung_batterie, liste, ladeleistung, aussentemperatur
    aussentemperatur = temperatur
    streckenlaenge = Route.strecke['zurückgelegte Distanz [km]'].iloc[-1] * 1000

    # Initialisierung der Schleife
    t = 0  # Zeit in s
    v_ist = 0.0  # Ist-Geschwindigkeit in m/s
    zurueckgelegte_distanz = 0.0  # zurückgelegte Strecke in m
    kumulierter_energieverbrauch = 0.0
    liste = []

    # Schleife, die läuft bis Umlauf beendet
    while zurueckgelegte_distanz < streckenlaenge:
        # TODO: Halt an Bushaltestelle (if-else: bremsen() vs. fahren())

        # in Abhängigkeit der bereits zurückgelegten Distanz werden aktuelle Steigung sowie DWPT-Ladeleistung ermittelt
        ladeleistung = Route.dwpt_ladeleistung(zurueckgelegte_distanz)
        steigung = Route.steigung(zurueckgelegte_distanz)

        if Route.haltestelle(zurueckgelegte_distanz):
            # TODO: Methodik:
            #  1. Geschwindigkeit unmittelbar vor Bushaltestelle
            #  2. Bremszeit errechnen
            #  3. Bremsweg errechnen
            #  4. Zeit errechnen, die Bus für 'Bremsweg' mit Geschwindigkeit benötigt hat
            #  5. Penaltysekunden (t_Brems - t) --> for-Schleife
            #  6. Rekuperationsenergie bei Bremsung errechnen (negativ)
            #  7. Energieverbrauch beim Fahren während t_Brems errechnen
            #  8. Energieverbrauch korrigieren: E = E_rekup - E_fahren
            # Es wird ermittelt, wie lange gebremst werden musste, um das Fahrzeug zu Stillstand zu bringen
            verzoegerung = 2.0
            bremszeit = anhalten(v_ist, verzoegerung)

            # Nachträglich wird ermittelt, welche Energiemenge rekuperiert wurde
            # Diese wird im Modell nun im Stillstand aufgenommen
            # TODO: Work In Progress

            # Der Bus muss stehen, sobald die Bushaltestelle erreicht ist.
            beschleunigung = 0.0
            v_ist = 0.0
            v_soll = 0.0

        else:
            v_soll = Route.v_soll(zurueckgelegte_distanz)

            # Berechnung des Energieverbrauchs
            energieverbrauch_im_intervall = energieverbrauch()

            # Aktualisieren des Gesamtenergieverbrauchs im Umlauf
            kumulierter_energieverbrauch += energieverbrauch_im_intervall

            # Gesammelte Daten abspeichern (wichtig: vor dem Aktualisieren des SoC)
            daten_sichern()

            # Laden bzw. Entladen der Batterie, Berechnung des neuen SoC
            soc = Batterie.state_of_charge(energieverbrauch_im_intervall)

            # Berechnung der zurückgelegten Strecke und der neuen Ist-Geschwindigkeit
            zurueckgelegte_distanz += 0.5 * beschleunigung * (zeit_intervall ** 2) + v_ist * zeit_intervall
            v_ist += beschleunigung * zeit_intervall
            t += zeit_intervall
            uhrzeit += datetime.timedelta(seconds=zeit_intervall)

    # Tabelle mit allen relevanten Daten des Umlaufs wird erstellt und zurückgegeben
    umlauf_tabelle = pd.DataFrame(liste)
    return umlauf_tabelle

def energieverbrauch():
    global soc, kumulierter_energieverbrauch, uhrzeit, t, zurueckgelegte_distanz, v_ist, v_soll, steigung, \
        beschleunigung, leistung_batterie, liste, ladeleistung, aussentemperatur

    # Der Fahrer wählt in Abhängigkeit von Soll- und Ist-Geschwindigkeit eine Beschleunigung oder Verzögerung aus
    beschleunigung = Fahrer.beschleunigung(v_ist, v_soll)

    # Ermittlung des Gesamtleistungsbedarfs
    fahrwiderstaende = Fahrzeug.fahrwiderstaende(v_ist, beschleunigung, steigung)
    benoetigte_leistung = Elektromotor.leistung(fahrwiderstaende,
                                                v_ist) + Nebenverbraucher.leistung(aussentemperatur) - ladeleistung

    leistung_batterie = Batterie.leistung(benoetigte_leistung)

    # Berechnung des Energieverbrauchs während des gewählten Zeitintervalls
    return leistung_batterie * zeit_intervall  # in Joule



def daten_sichern():
    # Sammle neu gewonnene Daten in Liste
    neue_zeile = {'Uhrzeit': datetime.datetime.strftime(uhrzeit, '%H:%M:%S'),
                  'Außentemperatur \n[°C]': aussentemperatur,
                  'Typ': 'Umlauf',
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
