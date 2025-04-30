import sys
from neaspec import context
import Nea.Client.SharedDefinitions as nea

neascan_console = sys.version_info.minor == 4

# create copy of most recent scan which is currently displayed
recent_params = context.Microscope.Py.Preview.ScanParamters.Spawn()

# create new ScanParameters for PsHet Imaging
new_params = context.Microscope.Py.CreateRoute2DScanParameters(
    areaWidth=5, # in µm
    areHeight=5, # in µm
    columns=100, # in px
    rows=100, # in px
).Result

# change scan to standard AFM mode and change other parameters
new_params.ScanMode = nea.ScanMode.Afm
new_params.TargetMillisecondsPerPixel = 10.2 # in ms/px

# check if system is in correct state to run an AFM scan
if context.Logic.Scan.CanExecute(new_params):
    
    # run scan and write results to database
    context.Logic.Scan.Execute(new_params)
    
else:
    # extract state of the system 
    # this works different in neaSCAN console and stand-alone connection
    state = context.Logic.CurrentState if neascan_console else nea.IPyLogic(context.Logic).CurrentState
    print("Incorrect system state", state)
