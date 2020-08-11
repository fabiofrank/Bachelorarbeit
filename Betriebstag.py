import datetime
import pandas as pd
import Fahrer
import Route
from Fahrzeugkomponenten import Fahrzeug, Nebenverbraucher, Batterie, Elektromotor

# TODO: Sicherstellen, das DWPT auch während Bushaltestelle/Ampel funktioniert!!!

# Variablen des Busbetriebs
zeit_intervall = 1
soc: float
t: int
zurueckgelegte_distanz: float
uhrzeit: datetime
aussentemperatur: float
status: str
v_ist: float
v_soll: float
steigung: float
beschleunigung: float
ladeleistung: float
leistung_em: float
leistung_nv: float
leistung_batterie: float
energieverbrauch_im_intervall: float
kumulierter_energieverbrauch: float
liste: list


# (Lade-)Pause an Start-/Zielhaltestelle
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
                      'Kumulierter Energieverbrauch nach Intervall [t, t+1) [KWh]': kumulierter_energieverbrauch / 3600000}
        liste.append(neue_zeile)
        soc = Batterie.state_of_charge(energieaufnahme)
        uhrzeit += datetime.timedelta(seconds=zeit_intervall)

    pause_tabelle = pd.DataFrame(liste)
    return pause_tabelle


# einzelner Umlauf des Busses
def umlauf(temperatur):
    global soc, kumulierter_energieverbrauch, uhrzeit, t, zurueckgelegte_distanz, v_ist, v_soll, steigung, \
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

        # in Abhängigkeit der bereits zurückgelegten Distanz werden aktuelle Steigung sowie DWPT-Ladeleistung ermittelt
        ladeleistung = Route.dwpt_ladeleistung(zurueckgelegte_distanz)

        # Erreicht der Bus eine Haltestelle, so hält er an, steht für 30 Sekunden und fährt wieder los
        if Route.haltestelle(zurueckgelegte_distanz):
            # Der Bus kommt zum Stehen
            anhalten()

            # TODO: Wie lange steht Bus an Haltestelle?
            # Der Bus steht 30s an der Haltestelle
            stehen(sekunden=30)

            # Nach dem Halt fährt der Bus wieder los
            # 20 Sekunden Fahrt, um zu verhindern, dass in gleichem Haltestellenabschnitt noch einmal gehalten wird
            for i in range(0, 20):
                fahren()

        # analog für Ampeln mit 20 Skunden Standzeit
        elif Route.ampel(zurueckgelegte_distanz):
            anhalten()
            stehen(sekunden=20)
            for i in range(0, 20):
                fahren()

        else:
            fahren()

    # Tabelle mit allen relevanten Daten des Umlaufs wird erstellt und zurückgegeben
    umlauf_tabelle = pd.DataFrame(liste)
    return umlauf_tabelle


# Berechnung des Energieverbrauchs bei geg. #TODO:
def energieverbrauch():
    global leistung_batterie, ladeleistung, leistung_em, leistung_nv

    # Ermittlung des Gesamtleistungsbedarfs
    fahrwiderstaende = Fahrzeug.fahrwiderstaende(v_ist, beschleunigung, steigung)
    leistung_em = Elektromotor.leistung(fahrwiderstaende, v_ist)
    leistung_nv = Nebenverbraucher.leistung(aussentemperatur)
    ladeleistung = Route.dwpt_ladeleistung(zurueckgelegte_distanz)
    benoetigte_leistung = leistung_em + leistung_nv - ladeleistung

    leistung_batterie = Batterie.leistung(benoetigte_leistung)

    # Berechnung des Energieverbrauchs während des gewählten Zeitintervalls
    return leistung_batterie * zeit_intervall  # in Joule


def daten_sichern():
    # Sammle neu gewonnene Daten in Liste
    neue_zeile = {'Uhrzeit': datetime.datetime.strftime(uhrzeit, '%H:%M:%S'),
                  'Zeit t \n[s]': t,
                  'Zurückgelegte Distanz \n[m]': zurueckgelegte_distanz,
                  'Außen-\ntemperatur \n[°C]': aussentemperatur,
                  'Typ': 'Umlauf',
                  'SoC zum Zeitpunkt t \n[%]': soc,
                  'Status': status,
                  'Ist-Geschwindigkeit zum Zeitpunkt t \n[km/h]': v_ist * 3.6,
                  'Soll-Geschwindigkeit zum Zeitpunkt t \n[km/h]': v_soll * 3.6,
                  'Steigung im Intervall [t, t+1) \n[%]': steigung,
                  'Gewählte Beschleunigung im Intervall [t, t+1) \n[m/s²]': beschleunigung,
                  'Empfangene Leistung mittels DWPT \n[kW]': ladeleistung / 1000,
                  'Motorleistung [kW]': leistung_em / 1000,
                  'Leistung der Nebenverbraucher [kW]': leistung_nv / 1000,
                  'Abgerufene Batterieleistung im Intervall [t, t+1) \n[kW]': leistung_batterie / 1000,
                  'Kumulierter Energieverbrauch nach Intervall [t, t+1) \n[kWh]': kumulierter_energieverbrauch / 3600000}
    liste.append(neue_zeile)


def fahren():
    global soc, kumulierter_energieverbrauch, uhrzeit, t, zurueckgelegte_distanz, v_ist, v_soll, steigung, \
        beschleunigung, energieverbrauch_im_intervall, status

    status = 'Fahren'
    steigung = Route.steigung(zurueckgelegte_distanz)
    v_soll = Route.v_soll(zurueckgelegte_distanz)

    # Der Fahrer wählt in Abhängigkeit von Soll- und Ist-Geschwindigkeit eine Beschleunigung oder Verzögerung aus
    beschleunigung = Fahrer.beschleunigung(v_ist, v_soll)

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


# Nachträglich wird ermittelt, welche Energiemenge bei der Bremsung vor der Haltestelle rekuperiert wurde
# Diese wird im Modell im Stillstand aufgenommen bis Zeit und Energieverbrauch korrigiert sind
def anhalten():
    global soc, kumulierter_energieverbrauch, uhrzeit, t, v_ist, v_soll, \
        beschleunigung, leistung_batterie, ladeleistung, leistung_em, leistung_nv, energieverbrauch_im_intervall, status

    # Ermittlung von Bremszeit und Bremsweg bei konstanter Bremsverzögerung
    bremsverzoegerung = 2.0
    bremszeit = v_ist / bremsverzoegerung
    bremsweg = 0.5 * bremsverzoegerung * (bremszeit ** 2)

    # Ermittlung des Zeitfehlers
    if v_ist == 0.0:
        fehlende_zeitintervalle = 0

    else:
        zusaetzliche_haltezeit = bremszeit - bremsweg / v_ist
        fehlende_zeitintervalle = round(zusaetzliche_haltezeit / zeit_intervall)

    # Ermittlung des Fehlers im Energieverbrauch
    beschleunigung = 0.0
    energieverbrauch_fahren = energieverbrauch()

    beschleunigung = -bremsverzoegerung
    rekuperationsenergie = energieverbrauch()

    energieverbrauch_fehler = rekuperationsenergie - energieverbrauch_fahren

    # Korrektur des Energieverbrauchs
    for i in range(0, fehlende_zeitintervalle):
        # Das Fahrzeug steht bis Zeit korrigiert ist
        status = 'Korrektursekunde'
        v_ist = 0.0
        v_soll = 0.0
        beschleunigung = 0.0

        # Während der zeitkorrigierenden, zusätzlichen Haltezeit wird eine konstante Rekuperationsleistung simuliert
        ladeleistung = 0.0
        leistung_nv = 0.0
        leistung_em = 0.0
        leistung_batterie = energieverbrauch_fehler / fehlende_zeitintervalle
        energieverbrauch_im_intervall = leistung_batterie * zeit_intervall
        kumulierter_energieverbrauch += energieverbrauch_im_intervall

        # Speichern der Daten, Aktualisieren von SoC, Zeit und Uhrzeit
        daten_sichern()
        soc = Batterie.state_of_charge(energieverbrauch_im_intervall)
        t += zeit_intervall
        uhrzeit += datetime.timedelta(seconds=zeit_intervall)


def stehen(sekunden):
    global soc, kumulierter_energieverbrauch, uhrzeit, t, leistung_batterie, leistung_nv, leistung_em, ladeleistung, \
        energieverbrauch_im_intervall, status

    anzahl_intervalle = int(sekunden / zeit_intervall)
    status = 'Halten'
    ladeleistung = Route.dwpt_ladeleistung(zurueckgelegte_distanz)

    for i in range(0, anzahl_intervalle):
        # Der Elektromotor dreht nicht, lediglich die Nebenverbraucher benötigen Leistung
        leistung_em = 0.0
        leistung_nv = Nebenverbraucher.leistung(aussentemperatur)
        benoetigte_leistung = leistung_nv - ladeleistung
        leistung_batterie = Batterie.leistung(benoetigte_leistung)

        # Berechnung des Energieverbrauchs
        energieverbrauch_im_intervall = leistung_batterie * zeit_intervall

        # Aktualisieren des Gesamtenergieverbrauchs im Umlauf
        kumulierter_energieverbrauch += energieverbrauch_im_intervall

        # Gesammelte Daten abspeichern (wichtig: vor dem Aktualisieren des SoC)
        daten_sichern()

        # Laden bzw. Entladen der Batterie, Berechnung des neuen SoC
        soc = Batterie.state_of_charge(energieverbrauch_im_intervall)

        # Aktualisieren von Zeit und Uhrzeit
        t += zeit_intervall
        uhrzeit += datetime.timedelta(seconds=zeit_intervall)
