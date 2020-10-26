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

datei1 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Rundkurs für Gartenschau\3 DWPT-Dimensionierung\Gartenschau_alleLadehaltestellen.xlsx'
daten_umlauf1 = pd.read_excel(datei1, sheet_name='1 Umlauf')
daten_pause1 = pd.read_excel(datei1, sheet_name='2 Pause')

soc_umlauf1 = daten_umlauf1['SoC zum Zeitpunkt t \n[%]'].to_numpy()
soc_pause1 = daten_pause1['SoC [%]'].to_numpy()
soc1 = np.concatenate((soc_umlauf1, soc_pause1))

datei2 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Rundkurs für Gartenschau\3 DWPT-Dimensionierung\Gartenschau_alleLadehaltestellenplus2Ampeln.xlsx'
daten_umlauf2 = pd.read_excel(datei2, sheet_name='1 Umlauf')
daten_pause2 = pd.read_excel(datei2, sheet_name='2 Pause')
soc_umlauf2 = daten_umlauf2['SoC zum Zeitpunkt t \n[%]'].to_numpy()
soc_pause2 = daten_pause2['SoC [%]'].to_numpy()
soc2 = np.concatenate((soc_umlauf2, soc_pause2))

datei3 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Rundkurs für Gartenschau\3 DWPT-Dimensionierung\Gartenschau_alleLadehaltestellenplus4Ampeln.xlsx'
daten_umlauf3 = pd.read_excel(datei3, sheet_name='1 Umlauf')
daten_pause3 = pd.read_excel(datei3, sheet_name='2 Pause')
soc_umlauf3 = daten_umlauf3['SoC zum Zeitpunkt t \n[%]'].to_numpy()
soc_pause3 = daten_pause3['SoC [%]'].to_numpy()
soc3 = np.concatenate((soc_umlauf3, soc_pause3))


fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

zeit = np.arange(0, 1201)
ax1.plot(zeit, soc1, label='400 m')
ax1.set_ylabel(r'$SoC$ / % $\longrightarrow$')
ax1.set_ylim([96.75,100.25])
ax1.grid()
ax1.legend(loc='lower left')
ax1.axvspan(0, 13, facecolor='0.9')
ax1.axvspan(190, 267, facecolor='0.9')
ax1.axvspan(553, 689, facecolor='0.9')
ax1.axvspan(809, 886, facecolor='0.9')
ax1.axvspan(1044, 1201, facecolor='0.9')

ax2.plot(zeit, soc2, 'tab:orange', label='500 m')
ax2.set_ylabel(r'$SoC$ / % $\longrightarrow$')
ax2.set_ylim([96.75,100.25])
ax2.grid()
ax2.legend(loc='lower left')
ax2.axvspan(0, 13, facecolor='0.9')
ax2.axvspan(190, 267, facecolor='0.9')
ax2.axvspan(429, 483, facecolor='0.9')
ax2.axvspan(553, 689, facecolor='0.9')
ax2.axvspan(809, 886, facecolor='0.9')
ax2.axvspan(1044, 1201, facecolor='0.9')

ax3.plot(zeit, soc3, 'tab:green', label='600 m')
ax3.set_xlabel(r'$t$ / \si{\second} $\longrightarrow$', color='black')
ax3.set_ylabel(r'$SoC$ / % $\longrightarrow$')
ax3.set_ylim([96.75,100.25])
ax3.grid()
ax3.legend()
ax3.axvspan(0, 13, facecolor='0.9')
ax3.axvspan(190, 267, facecolor='0.9')
ax3.axvspan(429, 483, facecolor='0.9')
ax3.axvspan(553, 689, facecolor='0.9')
ax3.axvspan(809, 886, facecolor='0.9')
ax3.axvspan(963, 1016, facecolor='0.9')
ax3.axvspan(1044, 1201, facecolor='0.9')
#ax.text(133, 92.5, 'DWPT-Zone', color='0.5', ha='center', va='center')
#ax.text(1558, 92.5, 'DWPT-Zone', color='0.5', ha='center', va='center')



fig.set_size_inches(7, 5)
fig.savefig(r'C:\Users\fabio\Studium\Bachelorarbeit\BA Latex\Latex_Bachelorarbeit\Bilder\SoC_Gartenschau_einzelnerUmlauf.pgf')
#plt.show()