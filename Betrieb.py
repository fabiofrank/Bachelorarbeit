import datetime
import pandas as pd
import Fahrer
import Route
from Fahrzeugkomponenten import Fahrzeug, Nebenverbraucher, Batterie, Elektromotor

# TODO: Sicherstellen, das DWPT auch während Bushaltestelle/Ampel funktioniert!!!

zeit_intervall = 1

# Initialisierung: Start des Betriebstags
soc = 100.0 # SoC beträgt bei Start der Simulation 100%
daten_uebersicht = []
daten_umlaeufe = []
aussentemperatur = 20.0 # TODO: variabel gestalten

# Variablen während des Busbetriebs
t: int
zurueckgelegte_distanz: float
uhrzeit: datetime.datetime
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
def pause(ende):
    global soc, kumulierter_energieverbrauch, uhrzeit, t, liste, ladeleistung
    print(datetime.datetime.strftime(uhrzeit, '%H:%M'), ': Pause gestartet.')
    # Initialisierung
    t = 0
    soc_vor_pause = soc
    uhrzeit_vor_pause = uhrzeit
    uhrzeit_nach_pause = datetime.datetime.strptime(ende, '%H:%M')
    liste = []
    kumulierter_energieverbrauch = 0.0  # in Joule
    wirkungsgrad_induktiv = 0.9 # TODO: benutzerfreundlich oben festlegen
    ladeleistung_spule = 25000  # in Watt # TODO: benutzerfreundlich oben festlegen
    ladeleistung = Fahrzeug.anzahl_spulen * ladeleistung_spule * wirkungsgrad_induktiv  # in Watt
    ladeleistung_batterie = Batterie.leistung(-ladeleistung)
    theoretische_energieaufnahme = ladeleistung_batterie * zeit_intervall  # in Joule

    # Pause läuft bis zu gegebener Uhrzeit (Beginn der nächsten Fahrt)
    while uhrzeit <= uhrzeit_nach_pause:
        # Der SoC von 100% nicht überschritten werden
        if (Batterie.inhalt * 3600000) - theoretische_energieaufnahme > (Batterie.kapazitaet * 3600000):
            energieaufnahme = (Batterie.inhalt - Batterie.kapazitaet) * 3600000
        else:
            energieaufnahme = theoretische_energieaufnahme

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
        t += zeit_intervall

    pause_tabelle = pd.DataFrame(liste)
    daten_umlaeufe.append(pause_tabelle)

    ergebnis_pause = {'Typ': 'Pause ', # TODO: Nummer
                      'Uhrzeit zu Beginn': datetime.datetime.strftime(uhrzeit_vor_pause, '%H:%M'),
                      'Uhrzeit am Ende': datetime.datetime.strftime(uhrzeit, '%H:%M'),
                      'Außentemperatur [°C]': aussentemperatur,
                      'SoC zu Beginn [%]': soc_vor_pause,
                      'SoC am Ende [%]': soc,
                      'Energieverbrauch des Intervalls [kWh]': kumulierter_energieverbrauch / 3600000}
    daten_uebersicht.append(ergebnis_pause)


# einzelner Umlauf des Busses
def umlauf():
    global soc, kumulierter_energieverbrauch, uhrzeit, t, zurueckgelegte_distanz, v_ist, v_soll, steigung, \
        beschleunigung, leistung_batterie, liste, ladeleistung, aussentemperatur, soc_vor_umlauf, uhrzeit_vor_umlauf
    print(datetime.datetime.strftime(uhrzeit, '%H:%M'), ': Umlauf gestartet.')
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

        # in Abhängigkeit der bereits zurückgelegten Distanz werden aktuelle Steigung sowie DWPT-Ladeleistung ermittelt
        ladeleistung = Route.dwpt_ladeleistung(zurueckgelegte_distanz)

        # Erreicht der Bus eine Haltestelle, so hält er an, steht für 30 Sekunden und fährt wieder los
        if Route.haltestelle(zurueckgelegte_distanz):
            # Der Bus kommt zum Stehen
            anhalten()

            # TODO: Wie lange steht Bus an Haltestelle?
            # Der Bus steht 30s an der Haltestelle
            stehen(30, 'Haltestelle')

            # Nach dem Halt fährt der Bus wieder los
            # 20 Sekunden Fahrt, um zu verhindern, dass in gleichem Haltestellenabschnitt noch einmal gehalten wird
            for i in range(0, 20):
                fahren()

        # Erreicht der Bus eine Ampel, so hält er an und steht 20 s lang und fährt wieder los
        elif Route.ampel(zurueckgelegte_distanz):
            anhalten()
            stehen(20, 'Ampel')
            for i in range(0, 20):
                fahren()

        # "Normalfall": Der Bus muss nicht anhalten und fährt einfach
        else:
            fahren()

    # Tabelle mit allen relevanten Daten des Umlaufs wird erstellt und zurückgegeben
    umlauf_tabelle = pd.DataFrame(liste)
    daten_umlaeufe.append(umlauf_tabelle)
    daten_sichern_uebersicht()


# Berechnung des Energieverbrauchs bei geg. Parametern Ist-Geschwindigkeit, Beschleunigung,
# Steigung, Außentemperatur, zurückgelegter Distanz
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
    theoretischer_energieverbrauch_im_intervall = leistung_batterie * zeit_intervall

    # Sonderfall: Im Falle von Energieaufnahme darf der SoC von 100% nicht überschritten werden
    if (Batterie.inhalt * 3600000) - theoretischer_energieverbrauch_im_intervall > (Batterie.kapazitaet * 3600000):
        realer_energieverbrauch_im_intervall = (Batterie.inhalt - Batterie.kapazitaet) * 3600000
    else:
        realer_energieverbrauch_im_intervall = theoretischer_energieverbrauch_im_intervall

    return realer_energieverbrauch_im_intervall  # in Joule

# TODO: Auslagerung in 'Ausgabe'
# Speichern der gewonnenen Daten als Dictionary, das einer Liste hinzugefügt wird
# Die Liste enthältjedes Zeitintervall des Umlaufs in Form eines Dictionarys
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

def daten_sichern_uebersicht():
    ergebnis_umlauf = {'Typ': 'Umlauf ',
                       'Uhrzeit zu Beginn': datetime.datetime.strftime(uhrzeit_vor_umlauf, '%H:%M'),
                       'Uhrzeit am Ende': datetime.datetime.strftime(uhrzeit, '%H:%M'),
                       'Außentemperatur [°C]': aussentemperatur,
                       'SoC zu Beginn [%]': soc_vor_umlauf,
                       'SoC am Ende [%]': soc,
                       'Energieverbrauch des Intervalls [kWh]': kumulierter_energieverbrauch / 3600000}
    daten_uebersicht.append(ergebnis_umlauf)


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


# Im Falle von Bushaltestellen sowie Ampeln muss der Bus zum Stehen kommen.
# Nachträglich wird ermittelt, welche Energiemenge bei der Bremsung vor der Haltestelle rekuperiert wurde.
# Diese wird im Modell im Stillstand aufgenommen bis Zeit und Energieverbrauch korrigiert sind.
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

# An Bushaltestellen sowie Ampeln muss der Bus eine bestimmte Zeit halten
# Klimatisierung/Heizung sowie weitere Nebenverbraucher verbrauchen weiter Energie
# Ggf. wird Energie induktiv aufgenommen
def stehen(sekunden, ampel_oder_haltestelle):
    global soc, kumulierter_energieverbrauch, uhrzeit, t, leistung_batterie, leistung_nv, leistung_em, ladeleistung, \
        energieverbrauch_im_intervall, status

    anzahl_intervalle = int(sekunden / zeit_intervall)
    status = 'Halten: ' + ampel_oder_haltestelle
    ladeleistung = Route.dwpt_ladeleistung(zurueckgelegte_distanz)

    for i in range(0, anzahl_intervalle):
        # Der Elektromotor dreht nicht, lediglich die Nebenverbraucher benötigen Leistung
        leistung_em = 0.0
        leistung_nv = Nebenverbraucher.leistung(aussentemperatur)
        benoetigte_leistung = leistung_nv - ladeleistung
        leistung_batterie = Batterie.leistung(benoetigte_leistung)

        # Berechnung des Energieverbrauchs
        # Im Falle von Energieaufnahme darf der SoC von 100% nicht überschritten werden
        theoretischer_energieverbrauch_im_intervall = leistung_batterie * zeit_intervall

        if (Batterie.inhalt * 3600000) - theoretischer_energieverbrauch_im_intervall > (Batterie.kapazitaet * 3600000):
            energieverbrauch_im_intervall = (Batterie.inhalt - Batterie.kapazitaet) * 3600000
        else:
            energieverbrauch_im_intervall = theoretischer_energieverbrauch_im_intervall

        # Aktualisieren des Gesamtenergieverbrauchs im Umlauf
        kumulierter_energieverbrauch += energieverbrauch_im_intervall

        # Gesammelte Daten abspeichern (wichtig: vor dem Aktualisieren des SoC)
        daten_sichern()

        # Laden bzw. Entladen der Batterie, Berechnung des neuen SoC
        soc = Batterie.state_of_charge(energieverbrauch_im_intervall)

        # Aktualisieren von Zeit und Uhrzeit
        t += zeit_intervall
        uhrzeit += datetime.timedelta(seconds=zeit_intervall)
