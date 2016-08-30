__author__ = 'John.Edenfield'

from Coal import Coal
from Air import Air
from Combustion import CombustionAir,FlueGas

# Define Coal
coal =Coal()
air =Air()
# Combustion Air
combustion_air =CombustionAir(coal,air,O2inFG=2.5)

flue_gas= FlueGas(coal,air,combustion_air.excess,combustion_air.moles)


eff=(coal.HHV + combustion_air.enthalpy(650) - flue_gas.enthalpy(790))/coal.HHV

print(eff)





