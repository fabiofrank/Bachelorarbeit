import numpy as np
import pandas as pd

hoehenprofil: pd.DataFrame
strecke: pd.DataFrame


# CSV-Datei aus Online-Tool "GPS-Visualizer" (Route in Google Maps erzeugt)
def hoehenprofil_einlesen(csv_datei):
    global hoehenprofil
    hoehenprofil = pd.read_csv(csv_datei, skiprows=4, skipinitialspace=True)


def strecke_einlesen(xlsx_datei):
    global strecke
    strecke = pd.read_excel(xlsx_datei)


# Funktion gibt die Zeile im Array zurück, in der sich das Fahrzeug gerade befindet
def momentane_position_hoehenprofil(distanz_in_m):
    distanz_in_km = distanz_in_m / 1000
    zeile = 0
    for i in hoehenprofil['distance (km)']:  # Iteration über die Spalte mit der zurückgelegten Distanz
        if i < distanz_in_km:
            zeile += 1
            continue
        elif i >= distanz_in_km:  # Die Schleife erreicht den übergebenen Streckenabschnitt
            return zeile


# Funktion gibt die Steigung in Prozent zurück, die auf einem bestimmten Streckenabschnitt auf der Route vorliegt
def steigung(distanz_in_m):
    distanz_in_km = distanz_in_m / 1000
    zeile = 0
    for i in hoehenprofil['distance (km)']:  # Iteration über die Spalte mit der zurückgelegten Distanz
        if i < distanz_in_km:
            zeile += 1
            continue
        elif i >= distanz_in_km:  # Die Schleife erreicht den übergebenen Streckenabschnitt
            break
    #print('Zeile: ', zeile)
    if zeile >= len(hoehenprofil['distance (km)']):
        steigung_in_prozent = 0.0
    elif np.isnan(hoehenprofil['slope (%)'][zeile]):
        steigung_in_prozent = 0.0
    else:
        steigung_in_prozent = hoehenprofil['slope (%)'][zeile]
    return steigung_in_prozent


# Die in der Route vorgegebene Soll-Geschwindigkeit wird ermittelt
def v_soll(distanz):
    zeile = momentane_position_strecke(distanz)
    geschwindigkeit = strecke['Soll-Geschwindigkeit ab hier [km/h]'][zeile] / 3.6
    return geschwindigkeit  # in m/s


# Ist DWPT-Marker in Route gesetzt, so wird die feste Ladeleistung von 25 kW zurückgegeben
def dwpt_ladeleistung(distanz_in_m):
    zeile = momentane_position_strecke(distanz_in_m)
    wirkungsgrad_dwpt = 0.8
    ladeleistung_spule = 25000.0 # Watt
    anzahl_spulen = 3
    if strecke['DWPT-Abschnitt?'][zeile] == 1:
        ladeleistung = anzahl_spulen * ladeleistung_spule * wirkungsgrad_dwpt  # Watt
    else:
        ladeleistung = 0.0
    return ladeleistung

# TODO: Haltestellen bzw. Haltezeiten, wenn Marker in Streckendatei


def momentane_position_strecke(distanz_in_m):
    distanz_in_km = distanz_in_m / 1000
    zeile = -1
    for i in strecke['zurückgelegte Distanz [km]']:
        if distanz_in_km >= i:
            zeile += 1
        elif distanz_in_km < i:
            return zeile
