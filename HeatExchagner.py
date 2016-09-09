__author__ = 'John.Edenfield'
from Combustion import Combustion
import math


class AirHeater():
    # Air heater heat exchanger
    flow = 'counter'

    def __init__(self,combustion, Ta_in, Ta_out, Tg_in, Tg_out):

        self.combustion = combustion

        self.Ta_in = Ta_in  # Temperature of air into the Air Heater: should be close to ambient temperature
        self.Ta_out= Ta_out # Temperature of air out of the Air Heater

        self._Tg_in = Tg_in  # gas temperature into the air heater (EEGT)
        self._Tg_out = Tg_out # gas temperature out of the heat exchanger with leakage
        self.leakage = 0

        # define optimization function
        def func():
            return self.Q_fg/self.lmtd -self.Q_ca/self.lmtd
        #Typical Air Heater Leakage should be about 3% but is unknown
        self.solve( func , "leakage",3,0.001)

        self.UA = self.Q_fg/self.lmtd

    @property
    def Tg_in(self):
        return self._Tg_in

    @Tg_in.setter
    def Tg_in(self,value):
        self._Tg_in = value

        # This will change Tg_out and Ta_out. Ta_in will remain the same.
        # both function 1 and function 2 should return zero
        def func1():

            return self.Q_ca - self.Q_fg

        def func2():
            T_g = (self.Tg_in + self.Ta_in) / 2
            self.solve(func1,"Ta_out",T_g,0.001)
            return self.Q_UA -self.Q_fg

        T_guess = (self.Ta_in + self.Tg_in) / 2 # Initial Guess of Tg_out

        self.solve(func2,"_Tg_out",T_guess,0.0001)

    @property
    def Tg_out(self):
        return self._Tg_out

    @Tg_out.setter
    def Tg_out(self,value):
        self._Tg_out = value

        # This will change Tg_out and Ta_out. Ta_in will remain the same.
        # both function 1 and function 2 should return zero
        def func1():

            return self.Q_ca - self.Q_fg

        def func2():
            T_g = (self.Tg_in + self.Ta_in) / 2
            self.solve(func1,"Ta_out",T_g,0.001)
            return self.Q_UA -self.Q_fg

        T_guess = (self.Ta_in + self.Tg_in) / 2 # Initial Guess of Tg_out

        self.solve(func2,"_Tg_in",T_guess,0.0001)


    @property
    def lmtd(self):

        dt1 = self.Tg_out_no_leak - self.Ta_in
        dt2 = self.Tg_in - self.Ta_out
        return (dt1 - dt2) / math.log(dt1 / dt2)

    @property
    def Q_UA(self):
        return self.UA * self.lmtd

    @property
    def Q_fg(self):
        return self.combustion.fg_sensible_h(self.Tg_in, self.Tg_out_no_leak)

    @property
    def Q_ca(self):
        return self.combustion.combustion_air_h(self.Ta_out, self.Ta_in)

    @property
    def Tg_out_no_leak(self):
        # Temperature of gas without leakage
        Cp_air = self.combustion.air.cp(self.Ta_in)
        Cp_fg =  self.combustion.fg_cp(self.Tg_out)

        return self.Tg_out+ self.leakage/100 *Cp_air/Cp_fg * (self.Tg_out-self.Ta_in)


    def solve(self,fx,prop,guess,delta):
    # Solve using secant method
        g = guess
        while True:
            setattr(self,prop,g)
            f0 = fx() #Solve Fx
            setattr(self,prop,g + delta)
            f1 = fx() #Solve Fx

            inc = f1 *- delta / (f0 - f1)
            if abs(f0) < 0.01:
                    setattr(self,prop,g-inc)
                    break

            g = g - inc

    def print(self):

        print(' UA ={:.2f} \n Q_fg = {:.2f}  --> Q_ca = {:.2f} --> Q_UA = {:.2f} \n lmtd = {:.2f} '.format(self.UA,self.Q_fg,self.Q_ca,self.Q_UA, self.lmtd))
        print(' Leakage = {:.2f} '.format(self.leakage))
        print(' Tg_in  = {:.2f}  -------> Tg_out_no_leak = {:.2f} '.format(self.Tg_in,self.Tg_out_no_leak))
        print('                                   Tg_out = {:.2f}'.format(self.Tg_out))
        print(' Ta_out = {:.2f} <---------------- Ta_in  = {:.2f}'.format(self.Ta_out,self.Ta_in))


