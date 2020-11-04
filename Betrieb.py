import datetime
import pandas as pd
from scipy import constants
import Fahrer
import Route
import DWPT
import Ausgabe
from Fahrzeugkomponenten import Fahrzeug, Nebenverbraucher, Batterie, Elektromotor

zeit_intervall = 1  # in Sekunden

# Initialisierung: Start des Betriebstags
soc = 100.0  # SoC beträgt bei Start der Simulation 100%
daten_uebersicht = []
daten_umlaeufe = []

# Variablen während des Busbetriebs
t: int
zurueckgelegte_distanz: float
uhrzeit: datetime.datetime
uhrzeit_vor_umlauf: datetime.datetime
soc_vor_umlauf: float
temperatur: float
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
haltezeit_ampel = 15 # 15 Sekunden, übernommen von Rogge, Wollny und Sauer (2015)


# (Lade-)Pause an Start-/Zielhaltestelle
def pause(ende, aussentemperatur):
    global soc, kumulierter_energieverbrauch, uhrzeit, t, liste, ladeleistung, leistung_nv, leistung_batterie, temperatur
    print(datetime.datetime.strftime(uhrzeit, '%H:%M'), ': Pause gestartet.')
    # Initialisierung
    t = 0
    temperatur = aussentemperatur
    soc_vor_pause = soc
    uhrzeit_vor_pause = uhrzeit
    uhrzeit_nach_pause = ende
    liste = []
    kumulierter_energieverbrauch = 0.0  # in Joule
    ladeleistung = DWPT.anzahl_spulen * DWPT.ladeleistung * DWPT.wirkungsgrad_statisch  # in Watt
    leistung_nv = Nebenverbraucher.leistung(temperatur)
    leistung_batterie = Batterie.leistung(leistung_nv - ladeleistung)
    theoretische_energieaufnahme = leistung_batterie * zeit_intervall  # in Joule

    # Sonderfall: Pause kann nicht stattfinden, da vorheriger Umlauf zu lange gebraucht hat
    if uhrzeit > uhrzeit_nach_pause:
        Ausgabe.daten_sichern_pause()
    else:
        # Pause läuft bis zu gegebener Uhrzeit (Beginn der nächsten Fahrt)
        while uhrzeit <= uhrzeit_nach_pause:
            # Der SoC von 100% nicht überschritten werden
            if (Batterie.inhalt * 3600000) - theoretische_energieaufnahme > (Batterie.kapazitaet * 3600000):
                energieaufnahme = (Batterie.inhalt - Batterie.kapazitaet) * 3600000
            elif (Batterie.inhalt * 3600000) - theoretische_energieaufnahme < 0:
                energieaufnahme = 0.0
            else:
                energieaufnahme = theoretische_energieaufnahme

            # Energie wird "verbraucht" bzw. aufgenommen (negativ)
            kumulierter_energieverbrauch += energieaufnahme

            # Abspeichern
            Ausgabe.daten_sichern_pause()

            # Aktualisieren der Größen
            soc = Batterie.state_of_charge(energieaufnahme)
            uhrzeit += datetime.timedelta(seconds=zeit_intervall)
            t += zeit_intervall

    pause_tabelle = pd.DataFrame(liste)
    daten_umlaeufe.append(pause_tabelle)

    ergebnis_pause = {'Typ': 'Pause ',
                      'Uhrzeit zu Beginn': datetime.datetime.strftime(uhrzeit_vor_pause, '%H:%M'),
                      'Uhrzeit am Ende': datetime.datetime.strftime(uhrzeit, '%H:%M'),
                      'Außentemperatur [°C]': temperatur,
                      'SoC zu Beginn [%]': soc_vor_pause,
                      'SoC am Ende [%]': soc,
                      'Energieverbrauch des Intervalls [kWh]': kumulierter_energieverbrauch / 3600000}
    daten_uebersicht.append(ergebnis_pause)


# einzelner Umlauf des Busses
def umlauf(fahrgaeste, aussentemperatur):
    global soc, kumulierter_energieverbrauch, uhrzeit, t, zurueckgelegte_distanz, status, v_ist, v_soll, steigung, \
        beschleunigung, leistung_batterie, liste, ladeleistung, temperatur, soc_vor_umlauf, uhrzeit_vor_umlauf, haltezeit_ampel
    print(datetime.datetime.strftime(uhrzeit, '%H:%M'), ': Umlauf gestartet.')
    Fahrzeug.anzahl_fahrgaeste = fahrgaeste
    temperatur = aussentemperatur
    soc_vor_umlauf = soc
    uhrzeit_vor_umlauf = uhrzeit

    streckenlaenge = Route.strecke['zurückgelegte Distanz [km]'].iloc[-1] * 1000

    # Initialisierung der Schleife
    t = 0  # Zeit in s
    v_ist = 0.0  # Ist-Geschwindigkeit in m/s
    zurueckgelegte_distanz = 0.0  # zurückgelegte Strecke in m
    kumulierter_energieverbrauch = 0.0
    liste = []

    # Schleife, die läuft bis Umlauf beendet
    while zurueckgelegte_distanz < streckenlaenge:

        # Erreicht der Bus eine Haltestelle, so hält er an, steht für 30 Sekunden und fährt wieder los
        if Route.haltestelle(zurueckgelegte_distanz):
            # Der Bus kommt zum Stehen
            anhalten()

            status = 'Halten: Bushaltestelle'
            zeile = Route.momentane_position_strecke(zurueckgelegte_distanz)
            geplante_abfahrt = uhrzeit_vor_umlauf + datetime.timedelta(
                minutes=Route.strecke['Fahrplan [Minuten nach Start]'][zeile])
            min_haltezeit = Route.strecke['Haltezeit [s]'][zeile]


            # Der Bus steht bis er wieder im Fahrplan ist, aber mindestens 20 Sekunden
            if uhrzeit < geplante_abfahrt:
                zeit_bis_geplante_abfahrt = (geplante_abfahrt - uhrzeit).seconds
                haltezeit = max(min_haltezeit, zeit_bis_geplante_abfahrt)
            else:
                haltezeit = min_haltezeit


            for i in range(0, int(haltezeit)):
                stehen()

            # Nach dem Halt fährt der Bus wieder los
            # Solange bis nächste Zeile in Inputtabelle erreicht

            while zurueckgelegte_distanz < 1000 * Route.strecke['zurückgelegte Distanz [km]'][zeile + 1]:
                fahren()

        # Erreicht der Bus eine Ampel, so hält er an und steht 15 s lang und fährt wieder los
        elif Route.ampel(zurueckgelegte_distanz):
            anhalten()
            status = 'Halten: Ampel'

            anzahl_intervalle = int(haltezeit_ampel / zeit_intervall)

            for i in range(0, anzahl_intervalle):
                stehen()

            # Nach dem Halt fährt der Bus wieder los
            # Solange bis nächste Zeile in Inputtabelle erreicht
            zeile = Route.momentane_position_strecke(zurueckgelegte_distanz)
            while zurueckgelegte_distanz < 1000 * Route.strecke['zurückgelegte Distanz [km]'][zeile + 1]:
                fahren()

        # "Normalfall": Der Bus muss nicht anhalten und fährt einfach
        else:
            fahren()

    # Tabelle mit allen relevanten Daten des Umlaufs wird erstellt und zurückgegeben
    umlauf_tabelle = pd.DataFrame(liste)
    daten_umlaeufe.append(umlauf_tabelle)
    Ausgabe.daten_sichern_uebersicht()


# Berechnung des Energieverbrauchs bei geg. Parametern Ist-Geschwindigkeit, Beschleunigung,
# Steigung, Außentemperatur, zurückgelegter Distanz
def energieverbrauch():
    global leistung_batterie, ladeleistung, leistung_em, leistung_nv

    # Ermittlung des Gesamtleistungsbedarfs
    fahrwiderstaende = Fahrzeug.fahrwiderstaende(v_ist, beschleunigung, steigung)
    leistung_em = Elektromotor.leistung(fahrwiderstaende, v_ist)
    leistung_nv = Nebenverbraucher.leistung(temperatur)
    ladeleistung = Route.dwpt_ladeleistung(zurueckgelegte_distanz, 'dynamisch')
    benoetigte_leistung = leistung_em + leistung_nv - ladeleistung

    leistung_batterie = Batterie.leistung(benoetigte_leistung)

    # Berechnung des Energieverbrauchs während des gewählten Zeitintervalls
    theoretischer_energieverbrauch_im_intervall = leistung_batterie * zeit_intervall

    # Sonderfall: Im Falle von Energieaufnahme darf der SoC von 100% nicht überschritten werden
    if (Batterie.inhalt * 3600000) - theoretischer_energieverbrauch_im_intervall > (Batterie.kapazitaet * 3600000):
        realer_energieverbrauch_im_intervall = (Batterie.inhalt - Batterie.kapazitaet) * 3600000
    elif (Batterie.inhalt * 3600000) - theoretischer_energieverbrauch_im_intervall < 0:
        realer_energieverbrauch_im_intervall = 0.0
    else:
        realer_energieverbrauch_im_intervall = theoretischer_energieverbrauch_im_intervall

    return realer_energieverbrauch_im_intervall  # in Joule


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
    Ausgabe.daten_sichern()

    # Laden bzw. Entladen der Batterie, Berechnung des neuen SoC
    soc = Batterie.state_of_charge(energieverbrauch_im_intervall)

    # Berechnung der zurückgelegten Strecke und der neuen Ist-Geschwindigkeit
    zurueckgelegte_distanz += 0.5 * beschleunigung * (zeit_intervall ** 2) + v_ist * zeit_intervall
    v_ist += beschleunigung * zeit_intervall
    if v_ist < 0:
        v_ist = 0.0  # Ist-Geschwindigkeit wird nicht kleiner 0
    t += zeit_intervall
    uhrzeit += datetime.timedelta(seconds=zeit_intervall)


# Im Falle von Bushaltestellen sowie Ampeln muss der Bus zum Stehen kommen.
# Nachträglich wird ermittelt, welche Energiemenge bei der Bremsung vor der Haltestelle rekuperiert wurde.
# Diese wird im Modell im Stillstand aufgenommen bis Zeit und Energieverbrauch korrigiert sind.
def anhalten():
    global soc, kumulierter_energieverbrauch, uhrzeit, t, v_ist, v_soll, \
        beschleunigung, leistung_batterie, ladeleistung, leistung_em, leistung_nv, energieverbrauch_im_intervall, status

    # Ermittlung von Bremszeit und Bremsweg bei konstanter Bremsverzögerung
    bremsverzoegerung = 0.19 * constants.g  # Kirchner, Schubert und Haas (2014)
    bremszeit = v_ist / bremsverzoegerung  # in Sekunden
    bremsweg = 0.5 * bremsverzoegerung * (bremszeit ** 2)

    # Ermittlung des Zeitfehlers
    if v_ist == 0.0:
        fehlende_zeitintervalle = 0

    else:
        zusaetzliche_haltezeit = bremszeit - bremsweg / v_ist
        fehlende_zeitintervalle = round(zusaetzliche_haltezeit / zeit_intervall)

    # Ermittlung des Fehlers im Energieverbrauch

    # 1) Energie, die verbraucht wurde, da das Modell gefahren ist (anstatt schon zu bremsen)
    beschleunigung = 0.0
    energieverbrauch_fahren = energieverbrauch() * ((bremsweg / v_ist) / zeit_intervall)

    # 2) Energie, die bei der Bremsung rekuperiert worden wäre
    energieverbrauch_bremsen = 0  # zu bestimmen
    for i in range(0, round(bremszeit)):
        beschleunigung = -bremsverzoegerung
        energieverbrauch_bremsen += energieverbrauch()
        v_ist += beschleunigung

    energieverbrauch_fehler_gesamt = energieverbrauch_bremsen - energieverbrauch_fahren

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
        leistung_batterie = energieverbrauch_fehler_gesamt / fehlende_zeitintervalle
        energieverbrauch_im_intervall = leistung_batterie * zeit_intervall
        kumulierter_energieverbrauch += energieverbrauch_im_intervall

        # Speichern der Daten, Aktualisieren von SoC, Zeit und Uhrzeit
        Ausgabe.daten_sichern()
        soc = Batterie.state_of_charge(energieverbrauch_im_intervall)
        t += zeit_intervall
        uhrzeit += datetime.timedelta(seconds=zeit_intervall)


# Klimatisierung/Heizung sowie weitere Nebenverbraucher verbrauchen weiter Energie
# Ggf. wird Energie induktiv aufgenommen
def stehen():
    global soc, kumulierter_energieverbrauch, uhrzeit, t, leistung_batterie, leistung_nv, leistung_em, ladeleistung, \
        energieverbrauch_im_intervall, status

    # Der Elektromotor dreht nicht, lediglich die Nebenverbraucher benötigen Leistung
    leistung_em = 0.0
    leistung_nv = Nebenverbraucher.leistung(temperatur)
    ladeleistung = Route.dwpt_ladeleistung(zurueckgelegte_distanz, 'statisch')
    benoetigte_leistung = leistung_nv - ladeleistung
    leistung_batterie = Batterie.leistung(benoetigte_leistung)

    # Berechnung des Energieverbrauchs
    # Im Falle von Energieaufnahme darf der SoC von 100% nicht überschritten werden
    theoretischer_energieverbrauch_im_intervall = leistung_batterie * zeit_intervall

    if (Batterie.inhalt * 3600000) - theoretischer_energieverbrauch_im_intervall > (Batterie.kapazitaet * 3600000):
        energieverbrauch_im_intervall = (Batterie.inhalt - Batterie.kapazitaet) * 3600000
    elif (Batterie.inhalt * 3600000) - theoretischer_energieverbrauch_im_intervall < 0:
        energieverbrauch_im_intervall = 0.0
    else:
        energieverbrauch_im_intervall = theoretischer_energieverbrauch_im_intervall

    # Aktualisieren des Gesamtenergieverbrauchs im Umlauf
    kumulierter_energieverbrauch += energieverbrauch_im_intervall

    # Gesammelte Daten abspeichern (wichtig: vor dem Aktualisieren des SoC)
    Ausgabe.daten_sichern()

    # Laden bzw. Entladen der Batterie, Berechnung des neuen SoC
    soc = Batterie.state_of_charge(energieverbrauch_im_intervall)

    # Aktualisieren von Zeit und Uhrzeit
    t += zeit_intervall
    uhrzeit += datetime.timedelta(seconds=zeit_intervall)
