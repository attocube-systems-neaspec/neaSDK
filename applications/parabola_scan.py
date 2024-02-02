import asyncio
import os
from datetime import datetime
from dataclasses import dataclass
import numpy as np
from nea_tools import connect, disconnect
import matplotlib.pyplot as plt
import h5py

#=====================================================================================================================
# This script 
# 1. connects to a neaSCOPE stand-alone 
# 2.1 runs a line-by-line scan of the parabolic mirror
# 2.2 records optical Amplitudes O0A - O5A and stores in an array
# 3. exports measured amplitdes as png.
#=====================================================================================================================
# Options for this script:
# 1) Connect to system 
HOST = "nea-server" # system to connect to. Default to "nea-server"
PATH_TO_DLL = "" # location of SDK files. Determined automatically on client PC

# 2) Options for Scan 
DISTANCE_X = 5000 # scan range in fast axis (x), in nm
DISTANCE_Y = 5000 # scan range in slow axis (y), in nm
DISTANCE_Z = 2500 # scan range in slow axis (z), in nm
RESOLUTION_X = 10 # pixels in fast axis (x)
RESOLUTION_Y = 10 # pixels in slow axis (y)
RESOLUTION_Z = 3 # pixels in slow axis (z)
SLEEP_TIMER = 0.2 # time to wait after each movement

# 3) Options for data export as png and hdf5
DIR= os.path.join(os.environ["HOMEPATH"],"Desktop","ParabolaScan") # directory to save images 
CMAP = "jet" # color scheme for generated images, see https://matplotlib.org/stable/users/explain/colors/colormaps.html
FNAME = "ParabolaScan" # beginning of file name of each image
#=====================================================================================================================

asyncio.run(connect(HOST,None,""))
from neaspec import context
from nea_tools.microscope.motors import Mirror

@dataclass
class ScanResult:
    """Dataclass to combine measured data of mirror scan"""
    o0:np.ndarray
    o1:np.ndarray
    o2:np.ndarray
    o3:np.ndarray
    o4:np.ndarray
    o5:np.ndarray
    coordinates:np.ndarray
    """Measured mirror xyz coordinates in nm"""

    def __iter__(self):
        return iter((self.o0,self.o1,self.o2,self.o3,self.o4,self.o5))

async def scan_mirror(dx, dy, dz, res_x, res_y, res_z, sleep_timer = 0.3):
    """
    Perform a line-by-line scanning movement of the parabolic mirror
    to spatially map the laser intensity in XY plane. Scanning area is a rectangular
    with current mirror motor position as center. Returns measured 
    optical amplitudes as numpy arrays in a dict. Dict keys are indeces of correspondic
    optical harmonic

    Args:
        dx (float): scan range in x axis, in nm
        dy (float): scan range in y axis, in nm
        dz (float): scan range in y axis, in nm
        res_x (int): number of steps in x axis
        res_y (int): number of steps in y axis
        res_z (int): number of steps in z axis
        sleep_timer (float): time to wait after each mirror movement

    Returns:
        results (ScanResult): containss measured optical amplitudes and corresponding xyz
                mirror coordinates. 
    """
    amp:"dict[int,np.ndarray]" = {}
    phase:"dict[int,np.ndarray]" = {}
    for harmonic in range(6):
        amp[harmonic] = np.zeros((res_z,res_y,res_x))
        phase[harmonic] = np.zeros((res_z,res_y,res_x))

    coords = np.zeros((res_z,res_y,res_x,3))
    with Mirror() as mirror:
        mirror.go_relative(-dx/2,-dy/2,-dz/2)
        await mirror.await_async()
        await asyncio.sleep(SLEEP_TIMER)
        x0,y0,z0 = mirror.absolute_position

        for iz in range(res_z):
            for iy in range(res_y):
                for ix in range(res_x):
                    x1,y1,z1 = coords[iz,iy,ix] = mirror.absolute_position
                    print(f"x={int(x1-x0)} nm, y={int(y1-y0)} nm, z={int(z1-z0)} nm, O2A={round(context.Microscope.Py.OpticalAmplitude[2],3)} mV")
                    for harmonic in range(6):
                        amp[harmonic][iz,iy,ix] = context.Microscope.Py.OpticalAmplitude[harmonic]
                        phase[harmonic][iz,iy,ix] = context.Microscope.Py.OpticalAmplitude[harmonic]
                    
                    mirror.go_relative(dx/res_x*(res_x+1)/res_x,0,0) # stepwise movement in x
                    await mirror.await_async()
                    await asyncio.sleep(sleep_timer)
                    
                    
                # measure how far mirror actually moved
                # move back in x this much, could be more or less than dx
                mirror.go_relative(x0-x1,dy/res_y*(res_y+1)/res_y,0) # stepwise movement in y and back to x0
                await mirror.await_async()
                await asyncio.sleep(SLEEP_TIMER)
                x1,y1,z1 = mirror.absolute_position
                print(f"x={int(x1-x0)} nm, y={int(y1-y0)} nm, z={int(z1-z0)} nm")

            # measure how far mirror actually moved
            # move back in y this much, could be more or less than dx
            mirror.go_relative(x0-x1,y0-y1,dz/res_z*(res_z+1)/res_z) # stepwise movement in z and back to x0,y0
            await mirror.await_async()
            await asyncio.sleep(SLEEP_TIMER)
            x1,y1,z1 = mirror.absolute_position
            print(f"x={int(x1-x0)} nm, y={int(y1-y0)} nm, z={int(z1-z0)} nm")

        # move back to approx center
        mirror.go_relative(-dx/2,-dy/2,-dz/2)
        await mirror.await_async()
        await asyncio.sleep(SLEEP_TIMER)

    amp_result = ScanResult(amp[0],amp[1],amp[2],amp[3],amp[4],amp[5],coords)
    phase_result = ScanResult(phase[0],phase[1],phase[2],phase[3],phase[4],phase[5],coords)
    return amp_result,phase_result

if __name__ == "__main__":
    NOW = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    try:
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        if not os.path.isdir(DIR):
            raise IOError(f"{DIR} is not a directory")
        amp,phase = asyncio.run(scan_mirror(DISTANCE_X,DISTANCE_Y,DISTANCE_Z,RESOLUTION_X,RESOLUTION_Y, RESOLUTION_Z, SLEEP_TIMER))

        with h5py.File(os.path.join(DIR,f"{FNAME}_{NOW}.h5"),'w') as file:
            for harmonic, (a,p) in enumerate(zip(amp,phase)):
                file.create_dataset(f"O{harmonic}",data=a*np.exp(1j*p))
            file.create_dataset("coordinates",data=amp.coordinates)

        for harmonic, array in enumerate(amp):
            plt.imsave(os.path.join(DIR,f"{FNAME}_O{harmonic}A_{NOW}.png"),array ,cmap=CMAP)
    finally:
        disconnect()
