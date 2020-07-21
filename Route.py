# TODO: v_soll in Datei integrieren, Funktion für v_soll schreiben analog zu steigung(distanz, route)
# TODO: route als globale Variable anstatt Funktionsargument?

import numpy as np
import pandas as pd

# CSV-Datei aus Online-Tool "GPS-Visualizer" (Route in Google Maps erzeugt)
# Datei soll vorher um Sollgeschwindigkeit sowie Marker für Bushaltestellen und DWPT-Streckenabschnitte ergänzt werden
# Aus der übergebenen CSV-Datei wird ein Array erzeugt

#TODO: pandas statt genfromtxt
def einlesen(csv_datei):
    return pd.read_csv(csv_datei, skiprows=4, skipinitialspace=True)
   # return np.genfromtxt(csv_datei, delimiter=';', names=True, skip_header=4)


# Funktion gibt die Zeile im Array zurück, in der sich das Fahrzeug gerade befindet
def momentane_position(distanz_in_m, route):
    distanz_in_km = distanz_in_m / 1000
    zeile = 0
    for i in route['distance (km)']:  # Iteration über die Spalte mit der zurückgelegten Distanz
        if i < distanz_in_km:
            zeile += 1
            continue
        elif i >= distanz_in_km:  # Die Schleife erreicht den übergebenen Streckenabschnitt
            return zeile

# Funktion gibt die Steigung in Prozent zurück, die auf einem bestimmten Streckenabschnitt auf der Route vorliegt
def steigung(distanz_in_m, route):
    zeile = momentane_position(distanz_in_m, route)
    if np.isnan(route['slope (%)'][zeile]) == True:
        return 0.0
    else:
        return route['slope (%)'][zeile]


# Die in der Route vorgegebene Soll-Geschwindigkeit wird ermittelt
def v_soll(distanz, route):
    # TODO: v_soll implementieren
    return 50 / 3.6

# Ist DWPT-Marker in Route gesetzt, so wird die feste Ladeleistung von 25 kW zurückgegeben
def dwpt_ladeleistung(distanz_in_m, route):
    zeile = momentane_position(distanz_in_m, route)
    if route['dwpt'][zeile] == 1:
        ladeleistung = 25000.0 # Watt
    else:
        ladeleistung = 0.0
    return ladeleistung