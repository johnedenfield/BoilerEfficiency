__author__ = 'John.Edenfield'
from IdealGas import SO2, CO2, N2, H2Ov, O2, CO


class Combustion:
    def __init__(self, coal, air, O2inFG=2.2, COinFG=200):
        self.air = air
        self.coal = coal

        # Combustion
        self.O2inFG = O2inFG
        self.COinFG = COinFG

    @property
    def combustion_air(self):
        return CombustionAir(self)

    @property
    def flue_gas(self):
        return FlueGas(self)



class CombustionAir:

    def __init__(self, combustion):
        self.air = combustion.air
        self.coal = combustion.coal

        # Combustion
        self.O2inFG = combustion.O2inFG

    @property
    def theoretical_air_moles(self):
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

        return O2_T / self.air.O2v_wb  # moles of theoretical air per lb of coal

    @property
    def theoretical_air_mass(self):
        return self.theoretical_air_moles * self.air.MW_wb

    @property
    def excess_air_moles(self):
        return self.theoretical_air_moles * self.O2inFG / ( self.air.O2v_wb - self.O2inFG)

    @property
    def excess_air_mass(self):
        return self.excess_air_moles * self.air.MW_wb

    @property
    def percent_excess_air(self):
        return self.excess_air_mass / self.mass * 100

    @property
    def moles(self):
        return self.theoretical_air_moles + self.excess_air_moles

    @property
    def mass(self):
        return self.moles * self.air.MW_wb


    def enthalpy(self, Tg):
        # Btu per lb coal burned
        return self.mass * self.air.enthalpy(Tg)

    def cp(self, Tg):
        return self.air.cp(Tg)




class FlueGas:

    def __init__(self, combustion):
        self.coal=combustion.coal
        self.air = combustion.air
        self.combustion_air=combustion.combustion_air
        self.COinFG=combustion.COinFG

    @property
    def moles(self):
        fg = dict()
        fg['CO2'] = (self.coal.CB / 100) / 12
        # Moles of SO2
        fg['SO2'] = (self.coal.S / 100) / 32
        # Moles of H2O
        fg['H2Of'] = (self.coal.H / 100) / 2 + (self.coal.H2O / 100) / 18

        fg['H2Oa'] = self.air.H2Ovv_wb / 100 * self.combustion_air.moles
        # Moles of O2
        fg['O2'] = self.air.O2v_wb / 100 * self.combustion_air.excess_air_moles
        # Moles of N2
        fg['N2'] = (self.coal.N / 100) / 28 + self.air.N2v_wb / 100 * self.combustion_air.moles

        fg['Total'] = fg['CO2'] + fg['SO2'] + fg['H2Of'] + fg['H2Oa'] + fg['O2'] + fg['N2']

        return fg

    @property
    def mass(self):
        fg_mass = dict()
        fg = self.moles

        # Mass of CO2
        fg_mass['CO2'] = fg['CO2'] * CO2.MW
        # Mass of SO2
        fg_mass['SO2'] = fg['SO2'] * SO2.MW
        # Mass of H2O from flue / Hydrogen Combustion
        fg_mass['H2Of'] = fg['H2Of'] * H2Ov.MW
        # Mass of H2O in combustion air
        fg_mass['H2Oa'] = fg['H2Oa'] * H2Ov.MW
        # Mass of O2
        fg_mass['O2'] = fg['O2'] * O2.MW
        # Mass of N2
        fg_mass['N2'] = fg['N2'] * N2.MW

        fg_mass['Total'] = fg_mass['CO2'] + fg_mass['SO2'] + fg_mass['H2Of'] + fg_mass['H2Oa'] + fg_mass['O2'] + \
                           fg_mass['N2']

        return fg_mass


    def co_losses(self):
        Hv = 4350.54  # Btu/lb
        return self.COinFG / 10E6 * self.moles['total'] * CO.MW * Hv


    def enthalpy(self, Tg, T_ref =77):
        h = dict()

        h['O2'] = O2.enthalpy(Tg, T_ref)
        h['N2'] = N2.enthalpy(Tg, T_ref)

        h['H2O'] = H2Ov.enthalpy(Tg, T_ref)

        h['SO2'] = SO2.enthalpy(Tg, T_ref)
        h['CO2'] = CO2.enthalpy(Tg, T_ref)

        # Latent Heat Loses due to moisture in fuel and hydrogen combustion
        fg_mass = self.mass

        sensible = h['O2'] * fg_mass['O2'] + h['N2'] * fg_mass['N2'] + h['H2O'] * (fg_mass['H2Oa'] + fg_mass['H2Of']) + \
                   h['SO2'] * fg_mass['SO2'] + h['CO2'] * fg_mass['CO2']

        latent = 1050.87 * fg_mass['H2Of']

        return sensible + latent


    def cp(self, Tg):
        cp = dict()

        cp['O2'] = O2.cp(Tg)
        cp['N2'] = N2.cp(Tg)
        cp['H2O'] = H2Ov.cp(Tg)
        cp['SO2'] = SO2.cp(Tg)
        cp['CO2'] = CO2.cp(Tg)

        fg = self.moles
        CP = cp['O2'] * fg['O2'] + cp['N2'] * fg['N2'] + cp['H2O'] * (fg['H2Oa'] + fg['H2Of']) + cp['SO2'] * fg['SO2'] + \
            cp['CO2'] * fg['CO2']

        return CP/fg['Total']