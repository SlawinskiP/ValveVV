from CoolProp.CoolProp import PropsSI
import math
import matplotlib.pyplot as plt
import numpy as np

p_op = 0.3                    #set pressure, barg
p_b = 1                       #backpressure, bara
T_w = 4.5                     #working temperature, K
T_op = 14.7                   #opening temperature, K
m = 2808                      #mass flow, kg/h
fluid = "helium"
K_dr = 0.55                   #derated coefficient of discharge, -

#Calculations:
def diameter(p_op, p_b, T_op, m, fluid, K_dr):
    p_r = (1.1 * p_op) + 1                                               #relieving pressure, bara
    Cp = PropsSI("CPMASS", "T", T_op, "P", p_r*10**5, fluid)             #specific heat at constant pressure, J/molK
    Cv = PropsSI("CVMASS", "T", T_op, "P", p_r*10**5, fluid)             #specific heat at constant volume, J/molK
    k = Cp / Cv                                                          #isentropic exponent of the gas, -
    L = p_b / p_r
    R = (2 / (k + 1))**(k / (k - 1))
    C = 3.948*math.sqrt(k * (2/(k + 1))**((k + 1)/(k - 1)))              #function of isentropic exponent, -
    M = PropsSI("M", "T", T_op, "P", p_r * 10 ** 5, fluid) * 1000        #molar mass, kg/kmol
    Z = PropsSI("Z", "T", T_op, "P", p_r * 10 ** 5, fluid)               #compressibility factor, -
    if L <= R:
        flow_character = "Critical flow occurs:"
        A = m / (p_r * C * K_dr * math.sqrt(M / (Z * T_op)))             #flow area of a safety valve, mm2
        d_min = math.sqrt(4 * A / 3.14)                                  #minimum bore area, mm
    else:
        flow_character = "Subritical flow occurs:"
        K_b = math.sqrt(((2 * k / (k - 1)) * ((p_b / p_r) ** (2 / k) - (p_b / p_r) ** ((k + 1) / k))) / (k * (2 / (k + 1)) ** ((k + 1) / (k - 1))))
        A = m / (p_r * C * K_dr * K_b * math.sqrt(M /(Z * T_op)))
        d_min = math.sqrt(4 * A / 3.14)
    return (flow_character, round(A, 2), round(d_min, 2))

print(diameter(p_op, p_b, T_op, m, fluid, K_dr)[0])
print("Minimum bore area: ", diameter(p_op, p_b, T_op, m, fluid, K_dr)[1], "mm2")
print("Minimum bore diameter: ", diameter(p_op, p_b, T_op, m, fluid, K_dr)[2], "mm")
