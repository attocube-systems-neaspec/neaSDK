from neaspec import context
import Nea.Client.SharedDefinitions as nea
from time import sleep

def move_delay_stage(depth):
    # put your code to mode stage here
    print(f"{depth}/{context.Microscope.Py.ScanParameters.ResolutionDepth}")
    sleep(0.1)

def on_scan_suspended(position):
    """
    Called every time when the controller called `Scan.SuspendToWaitForClient()`
    during a Storyboard scan.
    """
    try:
        row, col, depth = position.Row, position.Column, position.Depth
        move_delay_stage(depth)
    except Exception:
        return False
    
    return True

context.Logic.SuspendingScanToWaitForClient = nea.SuspendingScanToWaitForClient(on_scan_suspended)
