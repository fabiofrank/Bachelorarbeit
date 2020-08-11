from Fahrzeugkomponenten import Getriebe

#TODO: Wirkungsgrad aus Primove-Daten

effizienz: float
maximale_leistung: float


# Berechnung der Leistung des Elektromotors unter Berücksichtigung von Verlusten
def leistung(fahrwiderstaende, v_ist):
    if fahrwiderstaende < 0:
        benoetigte_leistung_em = fahrwiderstaende * v_ist * effizienz * Getriebe.effizienz
        if abs(benoetigte_leistung_em) <= maximale_leistung:
            reale_leistung_em = benoetigte_leistung_em
        else:
            reale_leistung_em = - maximale_leistung
    else:
        benoetigte_leistung_em = (fahrwiderstaende * v_ist) / (effizienz * Getriebe.effizienz)
        if benoetigte_leistung_em <= maximale_leistung:
            reale_leistung_em = benoetigte_leistung_em
        else:
            reale_leistung_em = maximale_leistung

    return reale_leistung_em
