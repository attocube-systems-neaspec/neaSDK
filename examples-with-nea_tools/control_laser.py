"""
Selecting, tuning and enabling emission of laser. Using nanoFTIR laser 
here, works similar for other tunable lasers like MIRcat
"""
from nea_tools.lasers import get_available_lasers

# make sure to be in nanoFTIR sphere so laser is available for selection
# context.Logic.ChangeSphere.Execute(nea.Sphere.Spectroscopy)

lasers = get_available_lasers()
if lasers.get('FemtoFiber'):
    nanoftir = lasers['FemtoFiber']
elif lasers.get('Mule'):
    nanoftir = lasers['Mule']
else:
    raise AttributeError("No nanoFTIR laser connected")
nanoftir.select()
nanoftir.tune('E') #  can be 'A' - 'E'

power = nanoftir.get_power()
print('Current Power on Powermeter:',power)

nanoftir.heal()

# 