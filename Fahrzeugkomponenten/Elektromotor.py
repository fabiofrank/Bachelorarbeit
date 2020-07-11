from Fahrzeugkomponenten import Getriebe

effizienz = 0.0

# TODO: Motorleistung durch Maximum begrenzen
# Berechnung der Leistung des Elektromotors unter Berücksichtigung von Verlusten
def leistung(fahrwiderstaende, v_ist):
    if fahrwiderstaende < 0:
        leistung_em = fahrwiderstaende * v_ist * effizienz * Getriebe.effizienz
    else:
        leistung_em = (fahrwiderstaende * v_ist) / (effizienz * Getriebe.effizienz)
    return leistung_em
