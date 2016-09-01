__author__ = 'John.Edenfield'

from Combustion import CombustionAir, FlueGas

class Boiler:


    def __init__(self, coal ,air, Ta_in, Tg_out, TF_out, O2inFg, COinFG):

        self.coal=coal
        self.air =air

        self.combustion_air=CombustionAir(coal=coal,air =air,O2inFg =O2inFg)

        self.flue_gas=FlueGas(coal,air, self.combustion_air.excess_moles,self.combustion_air.moles)




    def radiation_loss(QN,m_fuel):
        Crad =0.211

        return Crad * QN**0.7 *10E6 * 0.0009486 * 3600/m_fuel