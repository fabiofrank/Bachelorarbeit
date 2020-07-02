from numpy import genfromtxt


class Route:

    def __init__(self, csv_datei):
        self.route = genfromtxt(csv_datei, delimiter=',', names=True)

    def steigung(self, distanz):
        zeile = -1
        for i in self.route['distance_km']:  # Iteration über die Spalte mit der zurückgelegten Distanz
            zeile += 1
            if i < distanz:
                continue
            elif i >= distanz:  # Die Schleife erreicht den übergebenen Streckenabschnitt
                steigung_in_prozent = self.route['slope_'][zeile]
                break

        return steigung_in_prozent

