
from IdealGas import N2, O2, H2Ov

class Air:

    # Mole Fraction
    N2v_db = 79.05
    O2v_db = 20.95


    def __init__(self, ta=80,pa=14.6959, rh=60):
        # Standard Atmospheric Conditions as defined by the American Boiler Manufactures Association
        self.ta = ta
        self.pa = pa
        self.rh = rh


    @property
    def MW_db(self):
        # Molecular Weight dry base
        return N2.MW * self.N2v_db / 100 + O2.MW * self.O2v_db/100

    @property
    def humidity_ratio(self):
        # lbs H2O to lbs dry air
        pw = self.rh / 100 * H2Ov.psat_T(self.ta)

        return 0.62198 * pw / (self.pa - pw)

    @property
    def specific_humidity(self):
        # lb H2O to lbs moist air
        hr = self.humidity_ratio
        return hr / (1 + hr)

    @property
    def MW_wb(self):
        # Molecular Weight wet base
        sh = self.specific_humidity

        mf_N2 = N2.MW * self.N2v_db/100 / self.MW_db # Mass fraction of Nitrogen
        mf_O2 = O2.MW * self.O2v_db/100 / self.MW_db # Mass fraction of Oxygen

        mw = 1 / (mf_N2 / N2.MW + mf_O2 / O2.MW + sh / H2Ov.MW)

        return mw

    @property
    def molar_wet2dry(self):

        sh = self.specific_humidity
        num = (1-sh)/self.MW_db
        den = sh/H2Ov.MW +(1-sh)/self.MW_db

        return num/den


    @property
    def O2v_wb(self):
        # Volume of O2 wet bases = Moles of O2 Wet Bases
        return self.O2v_db * self.molar_wet2dry

    @property
    def N2v_wb(self):
        # Volume of O2 wet bases = Moles of O2 Wet Bases
        return self.N2v_db*self.molar_wet2dry

    @property
    def H2Ovv_wb(self):
        # Volume of O2 wet bases = Moles of O2 Wet Bases
        sh = self.specific_humidity
        return sh/H2Ov.MW*self.MW_wb*100

    def enthalpy(self,Tg):

        h_O2 = self.O2v_wb/100 *O2.enthalpy(Tg)
        h_N2 = self.N2v_wb/100 *N2.enthalpy(Tg)
        h_H2Ov = self.H2Ovv_wb/100 *H2Ov.enthalpy(Tg)

        return h_O2 + h_N2 + h_H2Ov