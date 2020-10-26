import matplotlib
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime

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

def uhrzeit_soc_array(datei):
    daten_dict = pd.read_excel(datei, sheet_name=None)
    del daten_dict['Übersicht Betriebstag']
    del daten_dict['Parameter']

    liste = []
    soc_array = np.array(liste)
    uhrzeit_array = np.array([])

    for tabellenblatt in daten_dict:
        umlauf_dataframe = daten_dict[tabellenblatt]
        uhrzeit_umlauf = umlauf_dataframe['Uhrzeit']
        uhrzeit_array = np.append(uhrzeit_array, uhrzeit_umlauf)
        uhrzeit_format = mdates.DateFormatter('%H:%M')

        if 'Umlauf' in tabellenblatt:
            soc_umlauf = umlauf_dataframe['SoC zum Zeitpunkt t \n[%]'].to_numpy()
        elif 'Pause' in tabellenblatt:
            soc_umlauf = umlauf_dataframe['SoC [%]'].to_numpy()
        soc_array = np.append(soc_array, soc_umlauf)

    datetimes_liste = []
    for i in range(0, len(uhrzeit_array)):
        datetimes_liste.append(datetime.strptime(uhrzeit_array[i], '%H:%M:%S'))
    datetimes_array = np.array(datetimes_liste)
    return (datetimes_array, soc_array)

################################################################################################################################
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
fig.set_size_inches(7, 6)

datei12 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_2Receiver_inklMittagspause.xlsx'
datei13 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_3Receiver_inklMittagspause.xlsx'
datei14 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Basisszenario\Basisszenario_Linie24_inklMittagspause.xlsx'
datei15 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_5Receiver_inklMittagspause.xlsx'
datei16 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_6Receiver_inklMittagspause.xlsx'

(x12, y12) = uhrzeit_soc_array(datei12)
(x13, y13) = uhrzeit_soc_array(datei13)
(x14, y14) = uhrzeit_soc_array(datei14)
(x15, y15) = uhrzeit_soc_array(datei15)
(x16, y16) = uhrzeit_soc_array(datei16)

def batterie_leer(y):
    index = 0
    for i in y:
        if i < 0.1:
            break
        index += 1

    for j in range(0,(len(y)-index)):
        y[index + j] = 0

batterie_leer(y12)
batterie_leer(y13)
batterie_leer(y14)
batterie_leer(y15)
batterie_leer(y16)



datei22 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_2Receiver.xlsx'
datei23 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_3Receiver.xlsx'
datei24 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Basisszenario\Basisszenario_Linie24_ohneMittagspause.xlsx'
datei25 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_5Receiver.xlsx'
datei26 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Empfängerspulen\Linie24_6Receiver.xlsx'

(x22, y22) = uhrzeit_soc_array(datei22)
(x23, y23) = uhrzeit_soc_array(datei23)
(x24, y24) = uhrzeit_soc_array(datei24)
(x25, y25) = uhrzeit_soc_array(datei25)
(x26, y26) = uhrzeit_soc_array(datei26)

batterie_leer(y22)
batterie_leer(y23)
batterie_leer(y24)
batterie_leer(y25)
batterie_leer(y26)

ax1.plot_date(x12, y12, '-', label='2 Empfänger')
ax1.plot_date(x13, y13, '-', label='3 Empfänger')
ax1.plot_date(x14, y14, '-', label='4 Empfänger (Basis)')
ax1.plot_date(x15, y15, '-', label='5 Empfänger')
ax1.plot_date(x16, y16, '-', label='6 Empfänger')
ax1.set_ylabel(r'$SoC$ / % $\longrightarrow$')
ax1.set_ylim(bottom=0)
ax1.grid()
ax1.set_title('mit Mittagspause')
# box = ax1.get_position()
# ax1.set_position([box.x0, box.y0 + box.height * 0.1,
#                  box.width, box.height * 0.9])

l22 = ax2.plot_date(x22, y22, '-', label='2 Empfänger')
l23 = ax2.plot_date(x23, y23, '-', label='3 Empfänger (D)')
l24 = ax2.plot_date(x24, y24, '-', label='4 Empfänger (Basis)')
l25 = ax2.plot_date(x25, y25, '-', label='5 Empfänger')
l26 = ax2.plot_date(x26, y26, '-', label='6 Empfänger')
ax2.set_ylabel(r'$SoC$ / % $\longrightarrow$')
ax2.set_ylim(bottom=0)
fmt = mdates.DateFormatter('%H:%M')
ax2.xaxis.set_major_formatter(fmt)
ax2.set_xlabel(r'$Uhrzeit\ \longrightarrow$')
ax2.grid()
ax2.set_title('ohne Mittagspause')

fig.set_size_inches(7, 5)
fig.subplots_adjust(bottom=0.2)
handles, labels = ax2.get_legend_handles_labels()
plt.figlegend(handles, labels, ncol=3, loc='lower center', bbox_to_anchor=(0.5, 0))
fig.savefig(r'C:\Users\fabio\Studium\Bachelorarbeit\BA Latex\Latex_Bachelorarbeit\Bilder\SoC_Receiver_mitohneMittagspause.pgf')
