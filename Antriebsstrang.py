import numpy as np
from scipy import constants

#physikalische Konstanten
g = constants.g

#feste Bus-Parameter
masse = 12000 #in kg
f_roll = 0.015 #Rollwiderstandbeiwert [ohne Einheit]

#Input: Ist-Geschwindigkeit in m/s, gewählte Beschleunigung in m/s² aus Fahrermodell
v_ist = 10.0
a_gewählt = 1.0
alpha = 5

def rollwiderstand():
    return rollwiderstand = masse * g * np.cos(alpha) * f_roll

fahrwiderstände = rollwiderstand() + beschleunigungswiderstand() + luftwiderstand(v_ist) + steigungswiderstand()
benötigte_leistung = fahrwiderstände * v_ist