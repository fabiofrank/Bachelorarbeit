from numpy import genfromtxt


# Einlesen der .csv-Datei mit der Routenplanung inkl. Distanz und Steigung
route = genfromtxt("Testdatensatz_10 Zeilen.csv", delimiter=',', names=True)

def steigung(distanz):
    zeile = -1
    for i in route['distance_km']: # Iteration über die Spalte mit der zurückgelegten Distanz
        zeile += 1
        if i < distanz:
            continue
        elif i >= distanz: # Die Schleife erreicht den übergebenen Streckenabschnitt
            steigung_in_prozent = route['slope_'][zeile]
            break

    return steigung_in_prozent
