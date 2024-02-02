from neaspec import context
import Nea.Client.SharedDefinitions as nea

# create copy of most recent scan which is currently displayed
recent_params = context.Microscope.Py.Preview.ScanParamters.Spawn()

# create new ScanParameters for AFM
new_params = context.Microscope.Py.CreateRoute2DScanParameters(
    areaWidth=5, # in µm
    areHeight=5, # in µm
    columns=100, # in px
    rows=100, # in px
)

# change to ContactMode and change other parameters
new_params.ScanMode = nea.ScanMode.ContactMode2D
new_params.TargetMillisecondsPerPixel = 10.2 # in ms/px

# run scan and write results to database
context.Logic.Scan.Execute(new_params)