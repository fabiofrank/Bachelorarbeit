import numpy as np
from scipy.interpolate import interp1d
from scipy import constants
from matplotlib import pyplot as plt
import matplotlib

# Wahl der Beschleunigung und Verzögerung analog zu Sinhuber, Rohlfs und Sauer (2012):
# "Study on power and energy demand for sizing the energy storage systems for electrified local public transport buses"

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

#Plot
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    #'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    'pgf.preamble': [
        r"\usepackage[latin1]{inputenc}",    # use utf8 fonts
        r"\usepackage[T1]{fontenc}",        # plots will be generated
        r"\usepackage[detect-all,locale=DE]{siunitx}",
        ]
})
fig, ax = plt.subplots(1, 1)
cmap = plt.get_cmap("tab10")
x1 = np.arange(0, 21)
x2 = np.arange(20, 60)
y1 = np.full(21, beschleunigung_interpoliert(20 / 3.6))
y2 = beschleunigung_interpoliert(x2 / 3.6)
plt.plot(x1, y1)
plt.plot(x2, y2, color=cmap(0))
ax.set_xlabel(r'$v_{Ist}$ / \si{\kilo\metre\per\hour}  $\longrightarrow$')
ax.set_ylabel(r'$a$ / \si{\metre\per\square\second} $\longrightarrow$')
plt.grid()
fig.set_size_inches(7, 4)
fig.savefig(r'C:\Users\fabio\Studium\Bachelorarbeit\BA Latex\Latex_Bachelorarbeit\Bilder\Beschleunigung_interpoliert.pgf')
#plt.show()


# geschwindigkeitsabhängige Wahl der Beschleunigung
def beschleunigung(v_ist, v_soll):
    if v_ist < v_soll:
        if v_ist <= 20 / 3.6:
            gewaehlte_beschleunigung = float(beschleunigung_interpoliert(20 / 3.6))
        elif v_ist >= 60 / 3.6:
            gewaehlte_beschleunigung = float(beschleunigung_interpoliert(60 / 3.6))
        else:
            gewaehlte_beschleunigung = float(beschleunigung_interpoliert(v_ist))

    elif v_ist > v_soll:
        gewaehlte_beschleunigung = -0.8
    else:
        gewaehlte_beschleunigung = 0.0

    return gewaehlte_beschleunigung  # in m/s²
