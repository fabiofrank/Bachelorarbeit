from numpy import genfromtxt

# TODO: v_soll in Datei integrieren, Methode für v_soll schreiben analog zu steigung(self, distanz)
class Route:

    def __init__(self, csv_datei):
        self.route = genfromtxt(csv_datei, delimiter=',', names=True)

    def steigung(self, distanz):
        global steigung_in_prozent
        distanz_in_km = distanz / 1000
        zeile = -1
        for i in self.route['distance_km']:  # Iteration über die Spalte mit der zurückgelegten Distanz
            zeile += 1
            if i < distanz_in_km:
                continue
            elif i >= distanz_in_km:  # Die Schleife erreicht den übergebenen Streckenabschnitt
                steigung_in_prozent = self.route['slope_'][zeile]
            return steigung_in_prozent


    def v_soll(self, distanz):
        # TODO: v_soll implementieren
        return 50 / 3.6
