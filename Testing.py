__author__ = 'John.Edenfield'

from Coal import Coal
from Air import Air
from HeatExchagner import AirHeater
from Combustion import Combustion
from Boiler import Boiler



coal=Coal()
air=Air()

boiler=Boiler (coal,air,80,650,780,280,2.5,200)



# Air Heater Energy balance
UA= 12 # Per lb of flue burned

# Known Values
Ta_in =  80  # Combustion air temperature is fixed at ambient temperature
Ta_out = 650
Tg_in  = 780  # EEGT
Tg_out = 285

