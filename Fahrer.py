import numpy as np
from scipy.interpolate import interp1d


# gefahrene Beschleunigungen in SORT-Zyklen:
# innerhalb von  15 m von 0 auf 20 km/h
# innerhalb von  45 m von 0 auf 30 km/h
# innerhalb von 100 m von 0 auf 40 km/h
# innerhalb von 170 m von 0 auf 50 km/h
# innerhalb von 300 m von 0 auf 60 km/h

# Berechnung der jeweiligen Beschleunigungen in den SORT-Zyklen
distanz_SORT = np.array([15, 45, 100, 170, 300])  # in m
geschwindigkeit_SORT = np.array([20, 30, 40, 50, 60]) / 3.6  # in m/s
beschleunigung_SORT = geschwindigkeit_SORT ** 2 / (2 * distanz_SORT)  # in m/s²

# lineare Interpolation der SORT-Beschleunigungswerte (in Abhängigkeit der Geschwindigkeit)
beschleunigung_interpoliert = interp1d(geschwindigkeit_SORT, beschleunigung_SORT)


# geschwindigkeitsabhängige Wahl der Beschleunigung
def beschleunigung(v_ist, v_soll):
    if v_ist < v_soll:
        if v_ist <= 20 / 3.6:
            gewaehlte_beschleunigung = beschleunigung_interpoliert(20 / 3.6)
        else:
            gewaehlte_beschleunigung = beschleunigung_interpoliert(v_ist)

    elif v_ist > v_soll:
        gewaehlte_beschleunigung = -0.8
    else:
        gewaehlte_beschleunigung = 0.0

    return gewaehlte_beschleunigung # in m/s²
