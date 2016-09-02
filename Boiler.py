__author__ = 'John.Edenfield'

from Combustion import Combustion
from HeatExchagner import AirHeater

class Boiler():


    def __init__(self, coal ,air, Ta_in,Ta_out,Tg_in, Tg_out, O2inFg, COinFG):

        self.combustion=Combustion()
        self.air_heater=AirHeater()
        self.air_heater.combustion=self.combustion


    @property
    def coal(self):
        return self.combustion.coal

    @coal.setter
    def coal(self,value):
        self.combustion.coal = value

    @property
    def air(self):
        return self.combustion.air

    @air.setter
    def air(self,value):
        self.combustion.air = value


    def efficiency(self):

        Ta = self.combustion.air.ta
        C1 = self.combustion.coal.enthalpy(Ta)

        Ta_in
        C2 = self.combustion.combustion_air_h( Air Heater Outlet)

        self.combustion.fg_sensible_h(Tg)
        self.combustion.fg_latent_h

    def radiation_loss(QN,m_fuel):
        Crad =0.211

        return Crad * QN**0.7 *10E6 * 0.0009486 * 3600/m_fuel