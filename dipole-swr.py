#!/usr/bin/python3
#===============================================
# See https://en.wikipedia.org/wiki/Dipole_antenna
#===============================================



from math import sin, cos, log
from scipy.special import sici
from scipy.constants import pi, c

def sin2(t):
    return sin(t)**2

def ci(t):
    '''cosine integral'''
    return sici(t)[1]

def si(t):
    '''sine integral'''
    return sici(t)[0]

# euler constant
gamma = 0.577215664901532

# impedance of free space
Z0 = 376.73031

# Real input impedance of antenna
def R(f, L, a):
    k = 2*pi*f/c/velocity

    return Z0 / (2*pi*sin2(k*L/2)) * (
        gamma
        + log(k*L)
        - ci(k*L)
        + .5 * sin(k*L) * (
            si(2*k*L)
            -2*si(k*L)
        )
        + .5 * cos(k*L) * (
            gamma
            + log(k*L/2)
            + ci(2*k*L)
            - 2*ci(k*L)
        )
    )

# Reactive input impedance of antenna
def X(f, L, a):
    k = 2*pi*f/c/velocity

    return Z0 / (4*pi*sin2(k*L/2)) * (
        2*si(k*L)
        + cos(k*L) * (
            2*si(k*L)
            - si(2*k*L)
        )
        -sin(k*L) * (
            2*ci(k*L)
            - ci(2*k*L)
            - ci(2*k*a**2/L)
        )
    )

# The value in ohms of the load
def Z(f, L, d):
    # Real and imaginary part of input impedance at the input terminals
    return complex(R(f, L, d), X(f, L, d))


def SWR(Z_l, Z_s):
    #Z_l load, The value in ohms of the load (typically an antenna)
    #Z_s source, The Characteristic impedance of the transmission line in ohms 
    reflection_coef = (Z_l - Z_s) / (Z_l + Z_s)
    return (1 + abs(reflection_coef)) / (1 - abs(reflection_coef))


# in Hz
f_lower = 135e6
f_upper = 140e6
step = 750e2

# in meters
# 36in is 91.44
#length = 0.965
length = 0.93
diameter = 0.00635
#diameter = 0.009525

#velocity factor
velocity = 0.90

# in ohms
source = complex(75)

f = f_lower
while f < f_upper:
    load = Z(f, length, diameter)
    print('    %6.3f MHz: SWR %4.2f, %5.1f + j%4.1f' % (f/1e6, SWR(load, source), load.real, load.imag))
    f += step
