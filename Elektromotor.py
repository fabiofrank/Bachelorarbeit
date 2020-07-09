import Getriebe

effizienz = 0.0

# Berechnung der Leistung des Elektrmotors unter Berücksichtigung von Verlusten
def leistung(fahrwiderstaende, v_ist):
    if fahrwiderstaende < 0:
        leistung = fahrwiderstaende * v_ist * effizienz * Getriebe.effizienz
    else:
        leistung = (fahrwiderstaende * v_ist) / (effizienz * Getriebe.effizienz)
    return leistung