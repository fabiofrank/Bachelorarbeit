import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'text.usetex': True,
    'pgf.rcfonts': False,
    'pgf.preamble': [
        r"\usepackage[latin1]{inputenc}",    # use utf8 fonts
        r"\usepackage[T1]{fontenc}",        # plots will be generated
        r"\usepackage[detect-all,locale=DE]{siunitx}",
        ]
})

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

datei1 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Basisszenario\Basisszenario_Linie24_inklMittagspause.xlsx'
daten_umlauf = pd.read_excel(datei1, sheet_name='3 Umlauf')
zeit = np.arange(0, 1627)
v_soll = daten_umlauf['Soll-Geschwindigkeit zum Zeitpunkt t \n[km/h]'].to_numpy()
v_ist = daten_umlauf['Ist-Geschwindigkeit zum Zeitpunkt t \n[km/h]'].to_numpy()

ax1.plot(zeit, v_soll)
ax1.set_ylabel(r'$v_{Soll}$ / \si{\kilo\metre\per\hour} $\longrightarrow$')
ax1.set_yticks(ticks=[15,30,50])
ax1.grid()
ax1.set_title('Vorgegebene Soll-Geschwindigkeit')

ax2.plot(zeit, v_ist)
ax2.set_xlabel(r'$t$ / \si{\second} $\longrightarrow$', color='black')
ax2.set_ylabel(r'$v_{Ist}$ / \si{\kilo\metre\per\hour} $\longrightarrow$')
ax2.set_yticks(ticks=[15,30,50])
ax2.grid()
ax2.set_title('Ist-Geschwindigkeit der Simulation')
#plt.legend()

fig.set_size_inches(7, 4)
fig.savefig(r'C:\Users\fabio\Studium\Bachelorarbeit\BA Latex\Latex_Bachelorarbeit\Bilder\Geschwindigkeitsprofil.pgf')
#plt.show()