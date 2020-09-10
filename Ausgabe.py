import pandas as pd
import xlsxwriter
import datetime
import Betrieb
import DWPT
from Fahrzeugkomponenten import Batterie, Elektromotor, Fahrzeug, Getriebe, Leistungselektronik, Nebenverbraucher

def daten_sichern_uebersicht():
    ergebnis_umlauf = {'Typ': 'Umlauf ',
                       'Uhrzeit zu Beginn': datetime.datetime.strftime(Betrieb.uhrzeit_vor_umlauf, '%H:%M'),
                       'Uhrzeit am Ende': datetime.datetime.strftime(Betrieb.uhrzeit, '%H:%M'),
                       'Außentemperatur [°C]': Betrieb.temperatur,
                       'SoC zu Beginn [%]': Betrieb.soc_vor_umlauf,
                       'SoC am Ende [%]': Betrieb.soc,
                       'Energieverbrauch des Intervalls [kWh]': Betrieb.kumulierter_energieverbrauch / 3600000}
    Betrieb.daten_uebersicht.append(ergebnis_umlauf)

def daten_sichern_pause():
    neue_zeile = {'Uhrzeit': datetime.datetime.strftime(Betrieb.uhrzeit, '%H:%M:%S'),
                  'Typ': 'Pause',
                  'Zeit [s]': Betrieb.t,
                  'SoC [%]': Betrieb.soc,
                  'Empfangene Leistung mittels DWPT [kW]': Betrieb.ladeleistung / 1000,
                  'Leistung der Nebenverbraucher [KW]': Betrieb.leistung_nv / 1000,
                  'Abgerufene Batterieleistung im Intervall [t, t+1) [kW]': Betrieb.leistung_batterie / 1000,
                  'Kumulierter Energieverbrauch nach Intervall [t, t+1) [KWh]': Betrieb.kumulierter_energieverbrauch / 3600000}
    Betrieb.liste.append(neue_zeile)

# Speichern der gewonnenen Daten des Umlaufs als Dictionary, das einer Liste hinzugefügt wird
# Die Liste enthält jedes Zeitintervall des Umlaufs in Form eines Dictionarys
def daten_sichern():
    # Sammle neu gewonnene Daten in Liste
    neue_zeile = {'Uhrzeit': datetime.datetime.strftime(Betrieb.uhrzeit, '%H:%M:%S'),
                  'Zeit t \n[s]': Betrieb.t,
                  'Zurückgelegte Distanz \n[m]': Betrieb.zurueckgelegte_distanz,
                  'Außen-\ntemperatur \n[°C]': Betrieb.temperatur,
                  'Typ': 'Umlauf',
                  'SoC zum Zeitpunkt t \n[%]': Betrieb.soc,
                  'Status': Betrieb.status,
                  'Ist-Geschwindigkeit zum Zeitpunkt t \n[km/h]': Betrieb.v_ist * 3.6,
                  'Soll-Geschwindigkeit zum Zeitpunkt t \n[km/h]': Betrieb.v_soll * 3.6,
                  'Steigung im Intervall [t, t+1) \n[%]': Betrieb.steigung,
                  'Gewählte Beschleunigung im Intervall [t, t+1) \n[m/s²]': Betrieb.beschleunigung,
                  'Empfangene Leistung mittels DWPT \n[kW]': Betrieb.ladeleistung / 1000,
                  'Motorleistung [kW]': Betrieb.leistung_em / 1000,
                  'Leistung der Nebenverbraucher [kW]': Betrieb.leistung_nv / 1000,
                  'Abgerufene Batterieleistung im Intervall [t, t+1) \n[kW]': Betrieb.leistung_batterie / 1000,
                  'Kumulierter Energieverbrauch nach Intervall [t, t+1) \n[kWh]': Betrieb.kumulierter_energieverbrauch / 3600000}
    Betrieb.liste.append(neue_zeile)

# Output als Excel-Dokument
def formatierung(name_simulation, daten_uebersicht, daten_umlaeufe):
    datei = 'Outputdateien/' + name_simulation + '.xlsx'

    workbook = xlsxwriter.Workbook(name_simulation)
    uebersicht_betriebstag = pd.DataFrame(daten_uebersicht)

    with pd.ExcelWriter(datei, engine='xlsxwriter') as writer:

        # Übersicht über Parameterwerte auf erstem Tabellenblatt
        parameterwerte = [{'Parameter [Einheit]': 'Anzahl an Empfängerspulen am Fahrzeug', 'Wert': DWPT.anzahl_spulen},
                          {'Parameter [Einheit]': 'Induktive Ladeleistung [kW]', 'Wert': DWPT.ladeleistung / 1000},
                          {'Parameter [Einheit]': 'Wirkungsgrad des statischen Ladens [-]', 'Wert': DWPT.wirkungsgrad_statisch},
                          {'Parameter [Einheit]': 'Wirkungsgrad des dynamischen Ladens [-]', 'Wert':DWPT.wirkungsgrad_dynamisch},
                          {'Parameter [Einheit]': 'Nutzbare Batteriekapazität [kW]', 'Wert':  Batterie.kapazitaet},
                          {'Parameter [Einheit]': 'Wirkungsgrad der Batterie [-]', 'Wert': Batterie.effizienz},
                          {'Parameter [Einheit]': 'Wirkungsgrad der Leistungselektronik [-]','Wert': Leistungselektronik.effizienz},
                          {'Parameter [Einheit]': 'Nennleistung des Elektromotors [kW]','Wert': Elektromotor.maximale_leistung / 1000},
                          {'Parameter [Einheit]': 'Wirkungsgrad des Elektromotors [-]', 'Wert': Elektromotor.effizienz},
                          {'Parameter [Einheit]': 'Wirkungsgrad des Getriebes [-]', 'Wert': Getriebe.effizienz},
                          {'Parameter [Einheit]': 'Leermasse des Fahrzeugs [kg]', 'Wert': Fahrzeug.masse_leer},
                          {'Parameter [Einheit]': 'Masse je Fahrgast [kg]', 'Wert': Fahrzeug.masse_je_fahrgast},
                          {'Parameter [Einheit]': 'Frontfläche des Fahrzeugs [m²]', 'Wert': Fahrzeug.stirnflaeche},
                          {'Parameter [Einheit]': 'Rollwiderstandsbeiwert [-]', 'Wert': Fahrzeug.f_roll},
                          {'Parameter [Einheit]': 'Luftwiderstandsbeiwert [-]', 'Wert': Fahrzeug.c_w},
                          {'Parameter [Einheit]': 'Konstante Leistung der Nebenverbraucher (ohne Klimatisierung) [kW]', 'Wert': Nebenverbraucher.leistung_sonstiges / 1000},
                          {'Parameter [Einheit]': 'Haltezeit an Ampeln [s]', 'Wert': Betrieb.haltezeit_ampel}]

        uebersicht_parameter = pd.DataFrame(parameterwerte)
        uebersicht_parameter.to_excel(writer, sheet_name='Parameter', index=False)

        # Übersicht über Betriebstag auf erstem Tabellenblatt
        uebersicht_betriebstag.to_excel(writer, sheet_name='Übersicht Betriebstag', index=False, startrow=1,
                                        header=False)

        # Formatierung
        workbook = writer.book

        format_ganzzahl = workbook.add_format({'num_format': '###,##0'})
        format_gleitzahl = workbook.add_format({'num_format': '###,##0.00'})
        format_ueberschrift = workbook.add_format({
            'text_wrap': True,
            'align': 'center',
            'valign': 'vcenter'})

        worksheet = writer.sheets['Übersicht Betriebstag']
        tabellenbereich = 'A1:G' + str(len(uebersicht_betriebstag['Typ']) + 1)
        ueberschriften = []
        for i in uebersicht_betriebstag.columns.values:
            ueberschriften.append({'header': i})
        worksheet.add_table(tabellenbereich, {'columns': ueberschriften,
                                              'style': 'Table Style Light 11'})
        worksheet.set_column('A:G', 20, format_ganzzahl)
        worksheet.set_row(0, None, format_ueberschrift)

        # Übersicht über einzelne Umläufe auf eigenen Tabellenblättern
        for i in range(0, len(daten_umlaeufe)):

            daten_umlaeufe[i].to_excel(writer, sheet_name=str(i + 1) + ' ' + daten_umlaeufe[i]['Typ'][0], index=False,
                                       startrow=1, header=False)
            worksheet = writer.sheets[str(i + 1) + ' ' + daten_umlaeufe[i]['Typ'][0]]

            if daten_umlaeufe[i]['Typ'][0] == 'Umlauf':
                tabellenbereich_umlauf = 'A1:P' + str(len(daten_umlaeufe[i]['Typ']) + 1)
            if daten_umlaeufe[i]['Typ'][0] == 'Pause':
                tabellenbereich_umlauf = 'A1:H' + str(len(daten_umlaeufe[i]['Typ']) + 1)

            ueberschriften_umlauf = []
            for j in daten_umlaeufe[i].columns.values:
                ueberschriften_umlauf.append({'header': j})
            worksheet.add_table(tabellenbereich_umlauf, {'columns': ueberschriften_umlauf,
                                                         'style': 'Table Style Light 11'})
            worksheet.set_column('A:P', 15, format_ganzzahl)
            worksheet.set_column('K:K', 15, format_gleitzahl)
            worksheet.set_row(0, None, format_ueberschrift)

    print('Simulationslauf "' + name_simulation + '" beendet.')