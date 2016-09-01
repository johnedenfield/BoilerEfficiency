__author__ = 'John.Edenfield'

from Coal import Coal
from Air import Air
from Combustion import Combustion
import math



# Calculate UA for the APH

# Measured Values

Tg_in = 780
Tg_out = 280
Ta_in = 80
Ta_out = 650


# Define Coal
coal = Coal()
air = Air()
combustion = Combustion(coal, air, O2inFG=3.5)

H = air.enthalpy(Ta_out, Ta_in)
q = (H * combustion.combustion_air.mass)

dt1 = Tg_out - Ta_in
dt2 = Tg_in - Ta_out

lmtd = (dt1 - dt2) / math.log(dt1 / dt2)

ua = q / lmtd

def find_T(ua, Tg_in, Ta_in, combustion):
    # Guess Ta_out

    mfg = combustion.flue_gas_mass['Total']
    ma = combustion.air_mass

    def find_Tg_out(q, Tg_in, T_guess, combustion):

        delta = 5
        while True:

            H0 = combustion.flue_gas_enthalpy(Tg_in, T_guess)
            H1 = combustion.flue_gas_enthalpy(Tg_in, T_guess+ delta)

            qFG0 = mfg * H0
            qFG1 = mfg * H1




            dq0 = qFG0 - q
            dq1 = qFG1 - q

            print('dq0={}, dq1={}'.format(dq0,dq1))


            if abs(dq0) < 0.01:
                break


            T_guess = (T_guess + delta) - dq1 * delta / (dq0 - dq1)


        return T_guess

    # need to guess a  Ta Out

    def find_Ta_out(ua, Ta_in, T_guess,combustion):

        H = combustion.air.enthalpy(T_guess, Ta_in)
        q = ma * H
        Tg_out_guess = Ta_in + 50

        Tg_out = find_Tg_out(q,Tg_in, Tg_out_guess,combustion)

        print(Tg_out)

        dt1 = Tg_out - Ta_in
        dt2 = Tg_in - Ta_out

        return (dt1 - dt2) / math.log(dt1 / dt2) - q / ua  # Should be equal to zero

    T_guess = Tg_in - 20

    delta =5
    while True:
        f0 = find_Ta_out(ua,Ta_in,T_guess,combustion)
        f1 = find_Ta_out(ua,Ta_in,T_guess+ delta,combustion)

        if f0 < 0.01:
            break

        T_guess = (T_guess + delta) - f1 * delta / (f0 - f1)

    return T_guess




eff = (coal.HHV + combustion.combustion_air.enthalpy(600) - combustion.flue_gas.enthalpy(850)) / coal.HHV


print(eff)



