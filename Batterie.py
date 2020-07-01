import Antriebsstrang
import Nebenverbraucher

kapazitaet_kWh = 350 # in kWh
kapazitaet = kapazitaet_kWh * 3600000
inhalt = kapazitaet # Initialisierung

leistung = Antriebsstrang.leistung + Nebenverbraucher.leistung
zeit_intervall = 1 # in Sekunden
energie = leistung * zeit_intervall
effizienz_batterie = 0.95

if energie < 0:
    delta = energie * effizienz_batterie
    inhalt -= zufluss
else:
    delta = energie / effizienz_batterie

inhalt -= delta
soc = inhalt / kapazitaet

print("SoC: ", soc)

