__author__ = 'John.Edenfield'
from IdealGas import SO2, CO2, N2, H2Ov, O2, CO
from Coal import Coal
from Air import Air

class Combustion():
    def __init__(self,O2inFg=2.5,COinFG =200):
        self.coal=Coal()
        self.air= Air()
        self.O2inFG = O2inFg
        self.COinFG = COinFG

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
        return self.theoretical_air_moles * self.O2inFG / (self.air.O2v_wb - self.O2inFG)

    @property
    def excess_air_mass(self):
        return self.excess_air_moles * self.air.MW_wb

    @property
    def percent_excess_air(self):
        return self.excess_air_mass / self.combustion_air_mass * 100

    @property
    def combustion_air_moles(self):
        return self.theoretical_air_moles + self.excess_air_moles

    @property
    def combustion_air_mass(self):
        return self.combustion_air_moles * self.air.MW_wb


    def combustion_air_h(self, Tg, T_ref=77):
        # Btu per lb coal burned
        return self.combustion_air_mass * self.air.enthalpy(Tg, T_ref)

    def combustion_air_cp(self, Tg):
        return self.air.cp(Tg)

    # Flue gas properties
    @property
    def fg_moles(self):
        fg = dict()
        fg['CO2'] = (self.coal.CB / 100) / 12
        # Moles of SO2
        fg['SO2'] = (self.coal.S / 100) / 32
        # Moles of H2O
        fg['H2Of'] = (self.coal.H / 100) / 2 + (self.coal.H2O / 100) / 18

        fg['H2Oa'] = self.air.H2Ovv_wb / 100 * self.combustion_air_moles
        # Moles of O2
        fg['O2'] = self.air.O2v_wb / 100 * self.excess_air_moles
        # Moles of N2
        fg['N2'] = (self.coal.N / 100) / 28 + self.air.N2v_wb / 100 * self.combustion_air_moles

        fg['Total'] = fg['CO2'] + fg['SO2'] + fg['H2Of'] + fg['H2Oa'] + fg['O2'] + fg['N2']

        return fg

    @property
    def fg_mass(self):
        fg_mass = dict()
        fg = self.fg_moles

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

    @property
    def co_losses(self):
        Hv = 4350.54  # Btu/lb
        return self.COinFG / 10E6 * self.fg_moles['total'] * CO.MW * Hv


    def fg_sensible_h(self, Tg, T_ref=77):
        # Btu / lb of Coal
        h = dict()

        h['O2'] = O2.enthalpy(Tg, T_ref)
        h['N2'] = N2.enthalpy(Tg, T_ref)

        h['H2O'] = H2Ov.enthalpy(Tg, T_ref)

        h['SO2'] = SO2.enthalpy(Tg, T_ref)
        h['CO2'] = CO2.enthalpy(Tg, T_ref)

        # Latent Heat Loses due to moisture in fuel and hydrogen combustion
        fg_mass = self.fg_mass

        sensible = h['O2'] * fg_mass['O2'] + h['N2'] * fg_mass['N2'] + h['H2O'] * (fg_mass['H2Oa'] + fg_mass['H2Of']) + \
                   h['SO2'] * fg_mass['SO2'] + h['CO2'] * fg_mass['CO2']


        return sensible

    @property
    def fg_latent_h(self):
        return 1050.87 * self.fg_mass['H2Of']

    def fg_cp(self, Tg):
        cp = dict()

        cp['O2'] = O2.cp(Tg)
        cp['N2'] = N2.cp(Tg)
        cp['H2O'] = H2Ov.cp(Tg)
        cp['SO2'] = SO2.cp(Tg)
        cp['CO2'] = CO2.cp(Tg)

        fg = self.fg_moles
        CP = cp['O2'] * fg['O2'] + cp['N2'] * fg['N2'] + cp['H2O'] * (fg['H2Oa'] + fg['H2Of']) + cp['SO2'] * fg['SO2'] + \
             cp['CO2'] * fg['CO2']

        return CP / fg['Total']


