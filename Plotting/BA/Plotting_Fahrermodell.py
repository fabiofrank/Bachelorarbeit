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
x = np.arange(0,71)
y1 = np.full(20, beschleunigung_interpoliert(20 / 3.6))
x2 = np.arange(20,61)
y2 = beschleunigung_interpoliert(x2 / 3.6)
y3 = np.full(10, beschleunigung_interpoliert(60 / 3.6))
y = np.concatenate([y1,y2,y3])
plt.plot(x, y)
ax.set_xlabel(r'$v_t$ / \si{\kilo\metre\per\hour}  $\longrightarrow$')
ax.set_ylabel(r'$a$ / \si{\metre\per\square\second} $\longrightarrow$')
plt.grid()
fig.set_size_inches(7, 4)
fig.savefig(r'C:\Users\fabio\OneDrive\Bachelorarbeit\BA Latex\Latex_Bachelorarbeit\Bilder\Beschleunigung_interpoliert.pgf')
