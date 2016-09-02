__author__ = 'John.Edenfield'


class Coal:
    def __init__(self, HHV=8800, C=50.82, S=0.21, H=3.49, H2O=27.3, N=0.65, O=13.02, Ash=4.51, CinAsh=2.5):
        self.HHV = HHV
        self.C = C
        self.S = S
        self.H = H
        self.N = N
        self.H2O = H2O
        self.O = O
        self.Ash = Ash
        self.CinAsh = CinAsh

        self.name ='Coal'

    @property
    def UBC(self):
        return self.CinAsh * self.Ash / (100.0 - self.CinAsh)

    @property
    def CB(self):
        return self.C - self.UBC

    @property
    def HHVc(self):
        # Higher Heating Value Calculated using Dulong's formula

        return 14544 * self.C/100 +62028*(self.H/100- self.O/100/8) + 4050*self.S/100


    def enthalpy(self, T):
        cp = 0.4063
        return cp * (T - 77)

    def ash_loss(self, T_fur=2400, T_fly=700, PerFlyAsh=80):
        cp_furn = 0.23901
        cp_fly = 0.20076

        h_fly = cp_fly * PerFlyAsh / 100 * self.Ash / 100 * (T_fur - 77)
        h_furn = cp_furn * (100 - PerFlyAsh) / 100 * self.Ash / 100 * (T_fly - 77)

        return h_fly + h_furn