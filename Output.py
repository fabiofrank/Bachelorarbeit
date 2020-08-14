import pandas as pd
# TODO: Tabellenblatt mit Übersicht über Parameterannahmen
# Output als Excel-Dokument
def formatierung(daten_uebersicht, daten_umlaeufe):
    uebersicht_betriebstag = pd.DataFrame(daten_uebersicht)

    with pd.ExcelWriter('Output.xlsx', engine='xlsxwriter') as writer:
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
                tabellenbereich_umlauf = 'A1:F' + str(len(daten_umlaeufe[i]['Typ']) + 1)

            ueberschriften_umlauf = []
            for j in daten_umlaeufe[i].columns.values:
                ueberschriften_umlauf.append({'header': j})
            worksheet.add_table(tabellenbereich_umlauf, {'columns': ueberschriften_umlauf,
                                                         'style': 'Table Style Light 11'})
            worksheet.set_column('A:P', 15, format_ganzzahl)
            worksheet.set_column('I:I', 15, format_gleitzahl)
            worksheet.set_row(0, None, format_ueberschrift)

    print('Simulationslauf beendet.')