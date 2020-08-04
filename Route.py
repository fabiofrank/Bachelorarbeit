# TODO: v_soll in Datei integrieren, Funktion für v_soll schreiben analog zu steigung(distanz, route)

import numpy as np
import pandas as pd

route: pd.DataFrame


# CSV-Datei aus Online-Tool "GPS-Visualizer" (Route in Google Maps erzeugt)
# Datei soll vorher um Sollgeschwindigkeit sowie Marker für Bushaltestellen und DWPT-Streckenabschnitte ergänzt werden
# Aus der übergebenen CSV-Datei wird ein Array erzeugt
# TODO: Excel statt csv?
def einlesen(csv_datei):
    global route
    route = pd.read_csv(csv_datei, skiprows=4, skipinitialspace=True)


# Funktion gibt die Zeile im Array zurück, in der sich das Fahrzeug gerade befindet
def momentane_position(distanz_in_m):
    distanz_in_km = distanz_in_m / 1000
    zeile = 0
    for i in route['distance (km)']:  # Iteration über die Spalte mit der zurückgelegten Distanz
        if i < distanz_in_km:
            zeile += 1
            continue
        elif i >= distanz_in_km:  # Die Schleife erreicht den übergebenen Streckenabschnitt
            return zeile


# Funktion gibt die Steigung in Prozent zurück, die auf einem bestimmten Streckenabschnitt auf der Route vorliegt
def steigung(distanz_in_m):
    zeile = momentane_position(distanz_in_m)
    if np.isnan(route['slope (%)'][zeile]) is True:
        return 0.0
    else:
        return route['slope (%)'][zeile]


# Die in der Route vorgegebene Soll-Geschwindigkeit wird ermittelt
def v_soll(distanz):
    # TODO: v_soll implementieren
    zeile = momentane_position(distanz)
    # route['v_soll (km/h)'][zeile] / 3.6
    return 50 / 3.6

# Ist DWPT-Marker in Route gesetzt, so wird die feste Ladeleistung von 25 kW zurückgegeben
def dwpt_ladeleistung(distanz_in_m):
    zeile = momentane_position(distanz_in_m)
    if route['dwpt'][zeile] == 1:
        ladeleistung = 25000.0  # Watt
    else:
        ladeleistung = 0.0
    return ladeleistung
