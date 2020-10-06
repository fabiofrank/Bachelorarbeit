from matplotlib import pyplot as plt
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
datei = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Basisszenario\Basisszenario_Linie24_inklMittagspause.xlsx'
umlauf = pd.read_excel(datei, sheet_name='3 Umlauf')
pause = pd.read_excel(datei, sheet_name='4 Pause')

leistung_umlauf = umlauf['Abgerufene Batterieleistung im Intervall [t, t+1) \n[kW]'].to_numpy()
leistung_pause = pause['Abgerufene Batterieleistung im Intervall [t, t+1) [kW]'].to_numpy()
leistung = np.concatenate((leistung_umlauf, leistung_pause))

leistung_reshaped = leistung.reshape((10,180))
leistung_summiert = np.sum(leistung_reshaped, axis=1)
leistung_3minuten = np.repeat(leistung_summiert, repeats=180) / 180

leistung_reshaped = leistung.reshape((30,60))
leistung_summiert = np.sum(leistung_reshaped, axis=1)
leistung_1minute = np.repeat(leistung_summiert, repeats=60) / 60

leistung_reshaped = leistung.reshape((90, 20))
leistung_summiert = np.sum(leistung_reshaped, axis=1)
leistung_20sekunden = np.repeat(leistung_summiert, repeats=20) / 20

zeit = np.arange(0, 1800)

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

ax1.plot(zeit, leistung)
ax1.set_ylabel(r'$P$ / kW $\longrightarrow$')
ax1.axvspan(0, 267, facecolor='0.9')
ax1.axvspan(1317, 1800, facecolor='0.9')
ax1.axhline(y=-68.02, linestyle=':', color='0.5')
ax1.axhline(y=11.29, linestyle=':', color='0.5')
ax1.set_ylim([-230, 230])
ax1.grid()
ax1.set_title('Batterieleistung (Intervallschritte im Simulationsmodell: 1 Sekunde)')

ax2.plot(zeit, leistung_1minute)
#ax2.set_xlabel(r'$t$ / s $\longrightarrow$', color='black', fontsize=15)
ax2.set_ylabel(r'$P$ / kW $\longrightarrow$')
ax2.axvspan(0, 266, facecolor='0.9')
ax2.axvspan(1317, 1800, facecolor='0.9')
ax2.grid()
ax2.text(133, 70, 'DWPT-Zone', color='0.5', ha='center', va='center')
ax2.text(1558, 70, 'DWPT-Zone', color='0.5', ha='center', va='center')
ax2.set_xlabel(r'$t$ / s $\longrightarrow$', color='black')
ax2.set_title('Mittlere Batterieleistung (60-Sekunden-Intervalle)')

#plt.show()

fig.set_size_inches(7, 4)
fig.savefig(r'C:\Users\fabio\Studium\Bachelorarbeit\BA Latex\Latex_Bachelorarbeit\Bilder\Leistung_Basisszenario.pgf')