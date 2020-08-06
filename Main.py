import pandas as pd
import datetime
import Betriebstag
from Fahrzeugkomponenten import Fahrzeug, Batterie, Leistungselektronik, Elektromotor, Getriebe
import Route

# Die festen Fahrzeugparameter werden festgelegt
Fahrzeug.masse = 12000.0  # in kg
Fahrzeug.stirnflaeche = 8.8  # in qm
Fahrzeug.f_roll = 0.015
Fahrzeug.c_w = 0.3
Batterie.kapazitaet = 0.8 * 200.0  # in KWh
Batterie.effizienz = 0.95
Leistungselektronik.effizienz = 0.95
Elektromotor.effizienz = 0.95
Elektromotor.maximale_leistung = 300000.0  # Watt
Getriebe.effizienz = 0.95

# Die Route des Umlaufs wird eingelesen
Route.hoehenprofil_einlesen('20200715070018-25131-data.csv')
Route.strecke_einlesen('Input.xlsx')

# Der SoC zu Beginn des Betriebstags wird festgelegt
Betriebstag.soc = 100.0
Batterie.inhalt = Batterie.kapazitaet * Betriebstag.soc / 100

# Es wird eingestellt, wie groß die Zeitschritte in der Simulation sein sollen
Betriebstag.zeit_intervall = 1  # in Sekunden

# Uhrzeit des Betriebsstarts angeben
uhrzeit = '09:00'  # Format hh:mm
Betriebstag.uhrzeit = datetime.datetime.strptime(uhrzeit, '%H:%M')

# TODO: Input Außentemperatur
# TODO: Ändert sich die Masse/Passagierzahl im Laufe des Betriebstags?
# TODO: Übersicht über Betriebstag: Welche Werte sind interessant?

daten_uebersicht = []
daten_umlaeufe = []

# Aneinanderreihen von Umläufen
for i in range(1, 6):
    print("Umlauf ", i, " gestartet.")
    soc_vor_umlauf = Betriebstag.soc
    uhrzeit_vor_umlauf = Betriebstag.uhrzeit
    aktueller_umlauf = Betriebstag.umlauf()
    daten_umlaeufe.append(aktueller_umlauf)

    ergebnis_umlauf = {'Typ': 'Umlauf ' + str(i),
                       'Uhrzeit zu Beginn': datetime.datetime.strftime(uhrzeit_vor_umlauf, '%H:%M'),
                       'Uhrzeit am Ende': datetime.datetime.strftime(Betriebstag.uhrzeit, '%H:%M'),
                       'SoC zu Beginn [%]': soc_vor_umlauf,
                       'SoC am Ende [%]': Betriebstag.soc,
                       'Energieverbrauch \ndes Intervalls [kWh]': Betriebstag.kumulierter_energieverbrauch / 3600000}
    daten_uebersicht.append(ergebnis_umlauf)

    print('Pause ', i, ' gestartet.')
    soc_vor_pause = Betriebstag.soc
    uhrzeit_vor_pause = Betriebstag.uhrzeit
    aktuelle_pause = Betriebstag.pause(laenge=300)
    daten_umlaeufe.append(aktuelle_pause)

    ergebnis_pause = {'Typ': 'Pause ' + str(i),
                      'Uhrzeit zu Beginn': datetime.datetime.strftime(uhrzeit_vor_pause, '%H:%M'),
                      'Uhrzeit am Ende': datetime.datetime.strftime(Betriebstag.uhrzeit, '%H:%M'),
                      'SoC zu Beginn [%]': soc_vor_pause,
                      'SoC am Ende [%]': Betriebstag.soc,
                      'Energieverbrauch \ndes Intervalls [kWh]': Betriebstag.kumulierter_energieverbrauch / 3600000}
    daten_uebersicht.append(ergebnis_pause)

    print('--------------------------------')

print('Übersicht erstellen.')

# Output als Excel-Dokument
# TODO: in Datei/Funktionen auslagern
uebersicht_betriebstag = pd.DataFrame(daten_uebersicht)

with pd.ExcelWriter('Output.xlsx', engine='xlsxwriter') as writer:
    # Übersicht über Betriebstag auf erstem Tabellenblatt
    uebersicht_betriebstag.to_excel(writer, sheet_name='Übersicht Betriebstag', index=False, startrow=1, header=False)

    # Formatierung
    workbook = writer.book

    format_ganzzahl = workbook.add_format({'num_format': '###,##0'})
    format_gleitzahl = workbook.add_format({'num_format': '###,##0.00'})
    format_ueberschrift = workbook.add_format({
        'text_wrap': True,
        'align': 'center',
        'valign': 'vcenter'})

    worksheet = writer.sheets['Übersicht Betriebstag']
    tabellenbereich = 'A1:F' + str(len(uebersicht_betriebstag['Typ']) + 1)
    ueberschriften = []
    for i in uebersicht_betriebstag.columns.values:
        ueberschriften.append({'header': i})
    worksheet.add_table(tabellenbereich, {'columns': ueberschriften,
                                          'style': 'Table Style Light 11'})
    worksheet.set_column('A:F', 20, format_ganzzahl)
    worksheet.set_row(0, None, format_ueberschrift)

    # Übersicht über einzelne Umläufe auf eigenen Tabellenblättern
    for i in range(0, len(daten_umlaeufe)):
        daten_umlaeufe[i].to_excel(writer, sheet_name=str(i + 1) + ' ' + daten_umlaeufe[i]['Typ'][0], index=False,
                                   startrow=1, header=False)
        worksheet = writer.sheets[str(i + 1) + ' ' + daten_umlaeufe[i]['Typ'][0]]

        if daten_umlaeufe[i]['Typ'][0] == 'Umlauf':
            tabellenbereich_umlauf = 'A1:L' + str(len(daten_umlaeufe[i]['Typ']) + 1)
        if daten_umlaeufe[i]['Typ'][0] == 'Pause':
            tabellenbereich_umlauf = 'A1:F' + str(len(daten_umlaeufe[i]['Typ']) + 1)

        ueberschriften_umlauf = []
        for j in daten_umlaeufe[i].columns.values:
            ueberschriften_umlauf.append({'header': j})
        worksheet.add_table(tabellenbereich_umlauf, {'columns': ueberschriften_umlauf,
                                                     'style': 'Table Style Light 11'})
        worksheet.set_column('A:L', 15, format_ganzzahl)
        worksheet.set_column('I:I', 15, format_gleitzahl)
        worksheet.set_row(0, None, format_ueberschrift)

