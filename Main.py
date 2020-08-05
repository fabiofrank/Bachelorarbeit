import pandas as pd
import Betriebstag
from Fahrzeugkomponenten import Fahrzeug, Nebenverbraucher, Batterie, Leistungselektronik, Elektromotor, Getriebe
import Route

# Die festen Fahrzeugparameter werden festgelegt
Fahrzeug.masse = 12000.0  # in kg
Fahrzeug.stirnflaeche = 8.8  # in qm
Fahrzeug.f_roll = 0.015
Fahrzeug.c_w = 0.3
Batterie.kapazitaet = 350.0  # in KWh
Batterie.effizienz = 0.95
Leistungselektronik.effizienz = 1.0
Elektromotor.effizienz = 0.9
Elektromotor.maximale_leistung = 300000.0 #Watt
Getriebe.effizienz = 1.0

# Die Route des Umlaufs wird eingelesen
Route.einlesen('20200715070018-25131-data.csv')

# Der SoC zu Beginn des Betriebstags wird festgelegt
Betriebstag.soc = 100.0
Batterie.inhalt = Batterie.kapazitaet * Betriebstag.soc / 100

# Es wird eingestellt, wie groß die Zeitschritte in der Simulation sein sollen
Betriebstag.zeit_intervall = 1  # in Sekunden

# TODO: Uhrzeit der einzelnen Umläufe?
# TODO: Input Außentemperatur
# TODO: Ändert sich die Masse/Passagierzahl im Laufe des Betriebstags?
# TODO: Übersicht über Betriebstag: Welche Werte sind interessant?

daten_uebersicht = []
daten_umlaeufe = []

# Aneinanderreihen von Umläufen
for i in range(1, 2):
    print("Umlauf ", i, " gestartet.")
    soc_vor_umlauf = Betriebstag.soc
    aktueller_umlauf = Betriebstag.umlauf(nummer=str(i))
    daten_umlaeufe.append(aktueller_umlauf)

    ergebnis_umlauf = {'Umlauf bzw. Pause': 'Umlauf ' + str(i), 'SoC zu Beginn [%]': soc_vor_umlauf,
                       'SoC am Ende [%]': Betriebstag.soc,
                       'Energieverbrauch des Intervalls [kWh]': Betriebstag.kumulierter_energieverbrauch / 3600000}
    daten_uebersicht.append(ergebnis_umlauf)

    print('Pause ', i, ' gestartet.')
    soc_vor_pause = Betriebstag.soc
    aktuelle_pause = Betriebstag.pause(nummer=str(i), laenge=300)
    daten_umlaeufe.append(aktuelle_pause)

    ergebnis_pause = {'Umlauf bzw. Pause': 'Pause ' + str(i), 'SoC zu Beginn [%]': soc_vor_pause,
                      'SoC am Ende [%]': Betriebstag.soc,
                      'Energieverbrauch des Intervalls [kWh]': Betriebstag.kumulierter_energieverbrauch / 3600000}
    daten_uebersicht.append(ergebnis_pause)

    print('--------------------------------')

print('Übersicht erstellen.')

uebersicht_betriebstag = pd.DataFrame(daten_uebersicht)
with pd.ExcelWriter('Output.xlsx', engine='xlsxwriter') as writer:
    workbook = writer.book
    format_ganzzahl = workbook.add_format({'num_format': '###,##0'})
    format_gleitzahl = workbook.add_format({'num_format': '###,##0.00'})

    uebersicht_betriebstag.to_excel(writer, sheet_name='Übersicht Betriebstag', index=False)
    worksheet = writer.sheets['Übersicht Betriebstag']
    worksheet.set_column('B:D', 19, format_ganzzahl)

    for i in range(0, len(daten_umlaeufe)):
        daten_umlaeufe[i].to_excel(writer, sheet_name=str(i + 1) + ' ' + daten_umlaeufe[i]['Typ'][0], index=False)
        worksheet = writer.sheets[str(i + 1) + ' ' + daten_umlaeufe[i]['Typ'][0]]
        worksheet.set_column('B:K', 19, format_ganzzahl)
        worksheet.set_column('H:H', 19, format_gleitzahl)
    writer.save()


