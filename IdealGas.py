__author__ = 'johnedenfield'
import math
# Ideal Gas

class IdealGas:


    def __init__(self):
        pass

    @classmethod
    def enthalpy(cls, Tg, T_ref = 77):
        # Reference Enthalpy:

        # change in enthalpy = the integral of the cp equation  a + bT + cT^2 +dT^3
        # a(T2-T1) + b/2 (T2^2-T1^2)  +C/3(T2^3 -T1^3) + d/4 (T2^4- T1 ^4)
        dH = cls.coef['a']*(Tg -T_ref) + \
                cls.coef['b']/2*(Tg**2 - T_ref**2) +\
                cls.coef['c']/3*(Tg **3 - T_ref**3) + \
                cls.coef['d']/4*(Tg **4 - T_ref**4)



        dH_eng = dH / cls.MW * 0.23884  # Return in BTU /lbm F

        return dH_eng

    @classmethod
    def cp(cls, Tg):
        Tg_K = (Tg-32)*5/9 + 237.15

        # Gas Enthalpy
        h= cls.coef['a'] + cls.coef['b'] * (Tg_K) +  cls.coef['c'] * (Tg_K ** 2 ) + cls.coef['d'] * (Tg_K ** 3 )

        h_eng = h / cls.MW * 0.23884  # Return in BTU /lbm F

        return h_eng


class O2(IdealGas):
    # Oxygen
    MW = 32
    coef = {'a': 25.48, 'b': 1.520E-2, 'c': -0.7155E-5, 'd': 1.312E-9}

    def __init__(self):
        pass


class N2(IdealGas):
    # Nitrogen
    MW = 28
    coef = {'a': 28.9, 'b': -0.1571E-2, 'c': 0.8081E-5, 'd': -2.873E-9}

    def __init__(self):
        pass


class H2Ov(IdealGas):
    # Water Vapor
    MW = 18
    coef = {'a': 32.24, 'b': 0.1923E-2, 'c': 1.055E-5, 'd': 7.469E-9}

    def __init__(self):
        pass

    @classmethod
    def psat_T(self, T):

        Tc =(T-32)*5/9

        ps = 610.78 * math.exp (Tc / (Tc + 238.3) * 17.2694)  # pressure in pascal

        return 0.000145038 * ps


class CO2(IdealGas):
    # Carbon Dioxide
    MW = 44
    coef = {'a': 22.26, 'b': 5.981E-2, 'c': -3.501E-5, 'd': 7.469E-9}

    def __init__(self):
        pass


class CO(IdealGas):
    # Carbon Monoxide
    MW = 28
    coef = {'a': 28.16, 'b': 0.1675E-2, 'c': 0.5372E-5, 'd': -2.222E-9}

    def __init__(self):
        pass


class SO2(IdealGas):
    # Sulfur Dioxide
    MW = 64
    coef = {'a': 25.78, 'b': 5.795E-2, 'c': -3.812E-5, 'd': 8.612E-9}

    def __init__(self):
        pass








