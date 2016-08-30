__author__ = 'John.Edenfield'
from IdealGas import SO2, CO2, N2, H2Ov, O2


class CombustionAir:
    def __init__(self, coal, air, O2inFG=3.5):
        self.air = air
        self.coal = coal

        self.O2inFG = O2inFG


    @property
    def theoretical_O2(self):
        # Returns the moles of O2 required per lb of coal fired
        # Coal = As Fired Coal

        # Moles O2 For Carbon Combustion
        O2_C = self.coal.CB / 12

        # Moles O2 For Sulfur Combustion
        O2_S = self.coal.S / 32

        # Moles O2 For Hydrogen Combustion

        O2_H = self.coal.H / 2 * 0.5

        O2_F = self.coal.O / 32

        O2_T = O2_C + O2_S + O2_H - O2_F

        return O2_T / 100  # moles O2 per lb of coal

    @property
    def theoretical(self):
        return self.theoretical_O2 * 100 / self.air.O2v_wb

    @property
    def excess(self):
        return self.theoretical * self.O2inFG / ( self.air.O2v_wb - self.O2inFG)

    @property
    def moles(self):
        return self.theoretical + self.excess

    @property
    def mass(self):
        return self.moles * self.air.MW_wb


    def enthalpy(self, Tg):
        # Btu per lb coal burned
        return self.mass * self.air.enthalpy(Tg)


class FlueGas:
    def __init__(self, coal, air, excess_air, combustion_air):
        self.CO2 = (coal.CB / 100) / 12
        # Moles of SO2
        self.SO2 = (coal.S / 100) / 32
        # Moles of H2O
        self.H2Of = (coal.H / 100) / 2 + (coal.H2O / 100) / 18

        self.H2Oa = air.H2Ovv_wb / 100 * excess_air
        # Moles of O2
        self.O2 = air.O2v_wb / 100 * excess_air
        # Moles of N2
        self.N2 = (coal.N / 100) / 28 + air.N2v_wb / 100 * combustion_air


    @property
    def moles(self):
        return self.CO2 + self.SO2 + self.N2 + self.H2Of + self.H2Oa + self.O2

    @property
    def mass(self):
        return self.CO2 * CO2.MW + self.SO2 * SO2.MW + self.N2 * N2.MW + (
                                                                         self.H2Of + self.H2Oa) * H2Ov.MW + self.O2 * O2.MW

    def enthalpy(self, Tg):
        n_total = self.moles

        h_O2 = self.O2 / n_total * O2.enthalpy(Tg)
        h_N2 = self.N2 / n_total * N2.enthalpy(Tg)
        h_H2Ov = (self.H2Oa + self.H2Of) / n_total * H2Ov.enthalpy(Tg)

        h_SO2 = self.SO2 / n_total * SO2.enthalpy(Tg)
        h_CO2 = self.CO2 / n_total * CO2.enthalpy(Tg)

        # Latent Heat Loses due to moisture in fuel and hydrogen combustion


        h_sens = (h_O2 + h_N2 + h_H2Ov + h_SO2 + h_CO2) * self.mass
        h_latent = 1050.87 * self.H2Of * 18

        return h_sens + h_latent


    def co_losses(self,CO,Tg):
        Hv = 4350.54 # Btu/lb
        return CO/10E6*self.moles*CO.MW*Hv
