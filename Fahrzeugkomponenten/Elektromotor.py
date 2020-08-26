from Fahrzeugkomponenten import Getriebe


#######################################################################################################################
# KONSTANTE PARAMETER, DIE FÜR DIE SIMULATION FESTGELEGT WERDEN MÜSSEN

# Nennleistung des Elektromotors in Watt
maximale_leistung = 160000.0 # Siemens 1DB2016-2NB06

# Wirkungsgrad des Elektromotors, konstant angenommen
effizienz = 0.82 # Mittelwert aus Primove-Datensatz

# Wirkungsgrad des Getriebes
Getriebe.effizienz = 0.98 # nach Absprache mit Markus Tesar 26.08.2020

#######################################################################################################################


# Berechnung der Leistung des Elektromotors unter Berücksichtigung von Verlusten
def leistung(fahrwiderstaende, v_ist):
    # Betrieb als Generator
    if fahrwiderstaende < 0:
        benoetigte_leistung_em = fahrwiderstaende * v_ist * effizienz * Getriebe.effizienz
        if abs(benoetigte_leistung_em) <= maximale_leistung:
            reale_leistung_em = benoetigte_leistung_em
        else:
            reale_leistung_em = - maximale_leistung

    # Betrieb als Motor
    else:
        benoetigte_leistung_em = (fahrwiderstaende * v_ist) / (effizienz * Getriebe.effizienz)
        if benoetigte_leistung_em <= maximale_leistung:
            reale_leistung_em = benoetigte_leistung_em
        else:
            reale_leistung_em = maximale_leistung

    return reale_leistung_em
