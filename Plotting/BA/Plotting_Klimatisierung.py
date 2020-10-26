import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib
# matplotlib.use("pgf")
# matplotlib.rcParams.update({
#     "pgf.texsystem": "pdflatex",
#     #'font.family': 'serif',
#     'text.usetex': True,
#     'pgf.rcfonts': False,
#     'pgf.preamble': [
#         r"\usepackage[latin1]{inputenc}",    # use utf8 fonts
#         r"\usepackage[T1]{fontenc}",        # plots will be generated
#         r"\usepackage[detect-all,locale=DE]{siunitx}",
#         ]
# })

# Aus Modelldaten des Primove-Projekts wird die Klimatisierungsleistung hergeleitet
inputdatei = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Fahrzeugkomponenten\Klimatisierungsdaten.xlsx'
daten_sommer = pd.read_excel(inputdatei, sheet_name='Sommertag')
daten_herbst = pd.read_excel(inputdatei, sheet_name='Herbsttag')
daten_winter = pd.read_excel(inputdatei, sheet_name='Wintertag')

# Winterdaten werden halbiert, da im betrachteten Bus mit einer deutlich effizienteren Heizug gearbeitet wird
# Symmetrie Sommer-Winter wird damit hergestellt
daten_winter_ohneKorrektur = np.copy(daten_winter['Heizleistung Mittelwert [kW]'].to_numpy())
daten_ohneKorrektur = pd.concat([daten_sommer, daten_winter, daten_herbst]).sort_values(by='Außentemperatur [°C]')
daten_winter['Heizleistung Mittelwert [kW]'] = 0.5 * daten_winter['Heizleistung Mittelwert [kW]']
daten_kumuliert = pd.concat([daten_sommer, daten_winter, daten_herbst])
daten_geordnet = daten_kumuliert.sort_values(by='Außentemperatur [°C]')

temperatur = daten_geordnet['Außentemperatur [°C]'].to_numpy()
heizleistung = daten_geordnet['Heizleistung Mittelwert [kW]'].to_numpy()
heizleistung_ohneKorrektur = daten_ohneKorrektur['Heizleistung Mittelwert [kW]'].to_numpy()

fit = np.polyfit(temperatur, heizleistung, 2)
heizleistung_funktion = np.poly1d(fit)
heizleistung_funktion_ohneKorrektur = np.poly1d(np.polyfit(temperatur, heizleistung_ohneKorrektur, 2))

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
x = np.arange(-15, 40)
y1 = heizleistung_funktion_ohneKorrektur(x)
y2 = heizleistung_funktion(x)

ax1.plot(daten_winter['Außentemperatur [°C]'].to_numpy(), daten_winter_ohneKorrektur, 'b.', label='Wintertag')
ax1.plot(daten_herbst['Außentemperatur [°C]'].to_numpy(), daten_herbst['Heizleistung Mittelwert [kW]'].to_numpy(), 'y.', label='Herbsttag')
ax1.plot(daten_sommer['Außentemperatur [°C]'].to_numpy(), daten_sommer['Heizleistung Mittelwert [kW]'].to_numpy(), 'r.', label='Sommertag')
ax1.plot(x, y1, label='quadratischer Fit')
ax1.set_xlabel(r'$\vartheta$ / \si{\degreeCelsius} $\longrightarrow$')
ax1.set_ylabel(r'$P_{\mathrm{HVAC}}$ / \si{\kW} $\longrightarrow$')
ax1.legend()
ax1.grid()
ax1.set_ylim(0, 14.5)
ax1.set_xticks(ticks=[-10, 0, 10, 20, 30, 40])
ax1.set_title('Primärdaten')


ax2.plot(daten_winter['Außentemperatur [°C]'].to_numpy(), daten_winter['Heizleistung Mittelwert [kW]'].to_numpy(), 'b.', label='Wintertag (Werte halbiert)')
ax2.plot(daten_sommer['Außentemperatur [°C]'].to_numpy(), daten_sommer['Heizleistung Mittelwert [kW]'].to_numpy(), 'r.', label='Sommertag')
ax2.plot(daten_herbst['Außentemperatur [°C]'].to_numpy(), daten_herbst['Heizleistung Mittelwert [kW]'].to_numpy(), 'y.', label='Herbsttag')
ax2.plot(x, y2, label='quadratischer Fit')
ax2.set_xlabel(r'$\vartheta$ / \si{\degreeCelsius} $\longrightarrow$')
ax2.set_xticks(ticks=[-10, 0, 10, 20, 30, 40])
ax2.legend()
ax2.grid()
ax2.set_ylim(0, 14.5)
ax2.set_title('nach Anpassung der Winterwerte')

fig.set_size_inches(7, 4)
#fig.savefig(r'C:\Users\fabio\Studium\Bachelorarbeit\BA Latex\Latex_Bachelorarbeit\Bilder\Klimatisierungsleistung.pgf')
plt.show()