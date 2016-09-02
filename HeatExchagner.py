__author__ = 'John.Edenfield'
from Combustion import Combustion
import math


class AirHeater():
    # Air heater heat exchanger
    flow = 'counter'

    def __init__(self,Ta_in, Ta_out, Tg_in, Tg_out, leakage=3):

        self.leakage = leakage  # Leakage %
        self.Ta_in = Ta_in  # Temperature of air into the Air Heater
        self.Ta_out= Ta_out

        self.Tg_in = Tg_in  # gas temperature into the air heater (EEGT)
        self.Tg_out= Tg_out

        self.combustion = Combustion()

        self.UA = self.Q_fg/self.lmtd


    def Solve_Ta_out(self):

        T_guess = (self.Tg_in + self.Ta_in) / 2

        delta = 0.001

        while True:

            self.Ta_out = T_guess
            f0 = self.Q_ca - self.Q_fg

            self.Ta_out = T_guess + delta
            f1 = self.Q_ca - self.Q_fg

            T_inc = f1 * -delta / (f0 - f1)
            if abs(f0) < 0.01:
                self.Ta_out = T_guess- T_inc
                break

            T_guess = T_guess - T_inc


    def Solve_Tg_out(self):

        delta = 0.001
        T_guess = (self.Ta_in + self.Tg_in) / 2

        while True:

            self.Tg_out = T_guess

            self.Solve_Ta_out()
            f0 = self.Q_UA - self.Q_fg

            self.Tg_out = T_guess + delta
            self.Solve_Ta_out()
            f1 = self.Q_UA - self.Q_fg

            T_inc = f1 *- delta / (f0 - f1)

            if abs(f0) < 0.01:
                self.Tg_out = T_guess - T_inc
                self.Solve_Ta_out()
                break

            T_guess = T_guess - T_inc

    @property
    def lmtd(self):

        dt1 = self.Tg_out - self.Ta_in
        dt2 = self.Tg_in - self.Ta_out

        return (dt1 - dt2) / math.log(dt1 / dt2)


    @property
    def Q_UA(self):
        return self.UA * self.lmtd

    @property
    def Q_fg(self):
        return self.combustion.fg_sensible_h(self.Tg_in, self.Tg_out)

    @property
    def Q_ca(self):
        return self.combustion.combustion_air_h(self.Ta_out, self.Ta_in)

    def print(self):

        print(' UA ={:.2f} \n Q_fg = {:.2f}  --> Q_ca = {:.2f} --> Q_UA = {:.2f} \n lmtd = {:.2f} '.format(self.UA,self.Q_fg,self.Q_ca,self.Q_UA, self.lmtd))
        print(' Tg_in  = {:.2f}  -------> Tg_out = {:.2f}'.format(self.Tg_in,self.Tg_out))
        print(' Ta_out = {:.2f} <-------  Ta_in  = {:.2f}'.format(self.Ta_out,self.Ta_in))


