# TODO: v_soll in Datei integrieren, Funktion für v_soll schreiben analog zu steigung(distanz, route)
# TODO: route als globale Variable anstatt Funktionsargument?

from numpy import genfromtxt


# Aus der übergebenen CSV-Datei wird ein Array erzeugt
def einlesen(csv_datei):
    return genfromtxt(csv_datei, delimiter=',', names=True)


# Funktion gibt die Steigung in Prozent zurück, die auf einem bestimmten Streckenabschnitt auf der Route vorliegt
def steigung(distanz_in_m, route):
    distanz_in_km = distanz_in_m / 1000
    zeile = 0
    for i in route['distance_km']:  # Iteration über die Spalte mit der zurückgelegten Distanz
        if i < distanz_in_km:
            zeile += 1
            continue
        elif i >= distanz_in_km:  # Die Schleife erreicht den übergebenen Streckenabschnitt
            return route['slope_'][zeile]


# Die in der Route vorgegebene Soll-Geschwindigkeit wird ermittelt
def v_soll(distanz, route):
    # TODO: v_soll implementieren
    return 50 / 3.6
