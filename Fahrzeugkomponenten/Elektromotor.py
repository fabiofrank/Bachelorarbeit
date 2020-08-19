from Fahrzeugkomponenten import Getriebe


#######################################################################################################################
# KONSTANTE PARAMETER, DIE FÜR DIE SIMULATION FESTGELEGT WERDEN MÜSSEN

# Nennleistung des Elektromotors in Watt
maximale_leistung = 250000.0 # TODO: Quelle finden oder Annahme treffen (Citaro), Auswirkungen vergleichen

# Wirkungsgrad des Elektromotors, konstant angenommen
effizienz = 0.82 # Mittelwert aus Primove-Datensatz

# Wirkungsgrad des Getriebes
Getriebe.effizienz = 0.95 # TODO: Quelle Getriebeverluste

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
