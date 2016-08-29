__author__ = 'johnedenfield'
import math
# Ideal Gas

class IdealGas:
    T_ref = 77

    def __init__(self):
        pass

    @classmethod
    def enthalpy(cls, Tg):
        h = cls.coef['a'] + cls.coef['b'] * (Tg - cls.T_ref) + \
            cls.coef['c'] * (Tg ** 2 - cls.T_ref ** 2) + cls.coef['d'] * (Tg ** 3 - cls.T_ref ** 3)

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


class Air:
    N2v_db = 79.05
    O2v_db = 20.95

    def __init__(self):
        pass

    @classmethod
    def MW_db(cls):
        # Molecular Weight dry base
        return N2.MW * cls.N2v_db / 100 + O2.MW * cls.O2v_db/100

    @classmethod
    def humidity_ratio(cls, t=75.0, pa=14.6959, rh=80.0):
        # lbs H2O to lbs dry air
        pw = rh / 100 * H2Ov.psat_T(t)

        return 0.62198 * pw / (pa - pw)

    @classmethod
    def specific_humidity(cls, t=75.0, pa=14.6959, rh=80.0):
        # lb H2O to lbs moist air
        hr = cls.humidity_ratio(t, pa, rh)
        return hr / (1 + hr)

    @classmethod
    def MW_wb(cls, t=75.0, pa=14.6959, rh=80.0):
        # Molecular Weight wet base
        sh = cls.specific_humidity(t, pa, rh)

        mf_N2 = N2.MW * cls.N2v_db/100 / cls.MW_db() # Mass fraction of Nitrogen
        mf_O2 = O2.MW * cls.O2v_db/100 / cls.MW_db() # Mass fraction of Oxygen

        mw = 1 / (mf_N2 / N2.MW + mf_O2 / O2.MW + sh / H2Ov.MW)

        return mw

    @classmethod
    def O2v_wb(cls, t=75.0, pa=14.6959, rh=80.0):
        # Volume of O2 wet bases = Moles of O2 Wet Bases
        sh = cls.specific_humidity(t, pa, rh)

        total_moles = (cls.O2v_db/100 +cls.N2v_db/100 + sh / H2Ov.MW)

        return cls.O2v_db/total_moles






