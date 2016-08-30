__author__ = 'John.Edenfield'

from Coal import Coal
from Air import Air
from Combustion import CombustionAir,FlueGas

# Define Coal
coal =Coal(C=80.31,H=4.47, S=1.54, O=2.85, N=1.38, H2O=2.9, Ash=6.55,CinAsh=5)
air =Air()
# Combustion Air
combustion_air =CombustionAir(coal,air,O2inFG=3.5)

flue_gas= FlueGas(coal,air,combustion_air.excess,combustion_air.moles)


eff=(coal.HHV + combustion_air.enthalpy(650) - flue_gas.enthalpy(780) - coal.ash_loss() )/coal.HHV

print(eff)
print(flue_gas.moles)
print(coal.CB)



