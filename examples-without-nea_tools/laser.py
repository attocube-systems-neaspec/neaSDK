from neaspec import context
import Nea.Client.SharedDefinitions as nea

mircat = context.Logic.AvailableLaserSources[nea.LaserSourceId.MIRcat]
if mircat is None:
    raise AttributeError("No MIRcat available")

# select laser
context.Logic.ChangeLaserSource.Execute(mircat)

# start emission
if mircat.LaserState != nea.LaserState.Emission:
    mircat.AllowEmission = True

# get allowed wavelength range, in um
total_range = mircat.SupportedTotalWavelengthRange
print(total_range.Low, total_range.High)

# tune laser to wavelength in um
mircat.TargetWavelength = 6.0

