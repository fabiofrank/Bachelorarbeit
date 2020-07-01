from numpy import genfromtxt

# Input: Fahrprofil mit Distanz und Steigung (next: v_soll für Streckenabschnitte)
route = genfromtxt("Testdatensatz_10 Zeilen.csv",delimiter=',',names=True)

print(route.dtype.names)
print(route['distance_km'])


def steigung(distanz):
    # bei gegebener zurückgelegter Strecke soll zurückgegeben werden, welche Steigung herrscht
    # Schleife durch Datei mit Routeninformationen?
    return 0

