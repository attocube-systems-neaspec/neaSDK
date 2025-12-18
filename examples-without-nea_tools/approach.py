import sys
from neaspec import context
from time import sleep
import Nea.Client.SharedDefinitions as nea

neascan_console = sys.version_info.minor == 4

def approach(setpoint=0.8):
    # exit if system is already in contact
    if context.Microscope.Py.IsRegulatorSetpointReachedZ:
        return 
    
    # exit if system is already approaching
    if context.Logic.IsApproachingSample:
        return 
    
    # check if approach is possible
    if context.Logic.ApproachSample.CanExecute(setpoint):
        context.Logic.ApproachSample.Exeucte(setpoint)
    else:
        state = context.Logic.CurrentState if neascan_console else nea.IPyLogic(context.Logic).CurrentState
        print("Cannot approach in current state", state)
        return

    # sleep until system has reached contact   
    while not context.Microscope.Py.IsRegulatorSetpointReachedZ:
        sleep(0.1, False)

def retract():
    if not context.Microscope.Py.IsRegulatorOutputEnabled:
        return
    context.Logic.DepartSample.Execute()
