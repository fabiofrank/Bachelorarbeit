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

fig, ax = plt.subplots(1, 1)

datei1 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Basisszenario\Basisszenario_Linie24_inklMittagspause.xlsx'
daten_umlauf = pd.read_excel(datei1, sheet_name='3 Umlauf')
daten_pause = pd.read_excel(datei1, sheet_name='4 Pause')
zeit = np.arange(0, 1800)
soc_umlauf = daten_umlauf['SoC zum Zeitpunkt t \n[%]'].to_numpy()
soc_pause = daten_pause['SoC [%]'].to_numpy()
soc = np.concatenate((soc_umlauf, soc_pause))
plt.plot(zeit, soc)

ax.axvspan(0, 266, facecolor='0.9')
ax.axvspan(1317, 1800, facecolor='0.9')
ax.text(133, 92.5, 'DWPT-Zone', color='0.5', ha='center', va='center')
ax.text(1558, 92.5, 'DWPT-Zone', color='0.5', ha='center', va='center')
ax.set_xlabel(r'$t$ / \si{\second} $\longrightarrow$', color='black')
ax.set_ylabel(r'$SoC$ / % $\longrightarrow$')
plt.grid()

fig.set_size_inches(7, 4)
fig.savefig(r'C:\Users\fabio\Studium\Bachelorarbeit\BA Latex\Latex_Bachelorarbeit\Bilder\SoC_einzelnerUmlauf.pgf')
#plt.show()