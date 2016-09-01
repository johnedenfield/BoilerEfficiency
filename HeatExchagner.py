__author__ = 'John.Edenfield'
import math

class HeatExchanger:

    def __init__(self):
        pass


    def lmtd(self, Th_in,Th_out,Tc_in,Tc_out):

        if self.flow == 'counter':
            dt1 = Th_out - Tc_in
            dt2 = Th_in  -Tc_out

        elif self.flow == 'parallel':
            dt1 = Th_in - Tc_in
            dt2 = Th_out  -Tc_out

        return (dt1-dt2)/math.log(math.e,dt1/dt2)

    def ua(self):

        pass



class AirHeater(HeatExchanger):
    # Air heater heat exchanger
    flow ='counter'

    def __init__(self,UA, Ta_in,combustion_air,flue_gas, leakage = 3 ):

        self.leakage = leakage # Leakage %
        self.Ta_in = Ta_in # Temperature of air into the Air Heater
        self.combustion_air = combustion_air
        self.flue_gas = flue_gas

    @property.setter
    def Tg_in(self, T):
        # Setting Tg in changes Tg_out and Ta_out based on UA

        mfg = self.flue_gas.mass['Total']
        ma = self.combustion_air.mass


        Tg_out = self.Tg_out  # Need To Guess an new Tg_out

        dH = self.flue_gas.enthalpy(T,Tg_out)

        Q = dH * self.flue_gas.mass['Total']

        Ta_out= self.Ta_out

        self.air.enthalpy(Ta_out, self.Ta_in )
        pass


    @property
    def Tg_out(self):
        pass

    @property
    def Ta_in(self):
        pass

    @property
    def Ta_out(self):
        pass


