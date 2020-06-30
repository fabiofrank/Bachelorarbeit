#Input: v_soll, v_ist
v_soll = 10.0
v_ist = 10.0

#Wahl der Beschleunigung
if v_ist < v_soll:
    gewaehlte_beschleunigung = 1.0
elif v_ist > v_soll:
    gewaehlte_beschleunigung = -0.8
else: gewaehlte_beschleunigung = 0.0