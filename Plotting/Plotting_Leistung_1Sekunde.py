from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime
datei = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Basisszenario\Basisszenario_Linie24_inklMittagspause.xlsx'
umlauf = pd.read_excel(datei, sheet_name='3 Umlauf')
pause = pd.read_excel(datei, sheet_name='4 Pause')

leistung_umlauf = umlauf['Abgerufene Batterieleistung im Intervall [t, t+1) \n[kW]'].to_numpy()
leistung_pause = pause['Abgerufene Batterieleistung im Intervall [t, t+1) [kW]'].to_numpy()
leistung = np.concatenate((leistung_umlauf, leistung_pause))

leistung_reshaped = leistung.reshape((360,5))
leistung_summiert = np.sum(leistung_reshaped, axis=1)
leistung_minute = np.repeat(leistung_summiert, repeats=5) / 5

zeit = np.arange(0, 1800)

fig, ax = plt.subplots(1, 1)

ax.plot(zeit, leistung)
ax.set_xlabel(r'$t$ / s $\longrightarrow$', color='black', fontsize=15)
ax.set_ylabel(r'$P$ / kW $\longrightarrow$', fontsize=15)
ax.grid()

ax.axhline(y=-68.01, linestyle=':', color='gray')
ax.axhline(y=11.29, linestyle=':', color='gray')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
#plt.legend()
plt.show()