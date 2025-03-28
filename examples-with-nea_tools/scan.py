"""
Run standard Tapping AFM scan and nano FTIR spectrum.
"""
from nea_tools.logic import scan

def print_all_scanmodes():
    for mode in scan.SCANMODES:
        print(mode)

def scan_tapping_afm():
    with scan.Afm(Name = "Standard Tapping AFM", # name displayed in project browser
                PhysicalOffsetX = 50, # central position in x, in um
                PhysicalOffsetY = 50, # central position in y, in um
                PhysicalSizeX = 5, # size in x, in um
                PhysicalSizeY = 5, # size in y, in um
                Angle = 0, # angle of scan, in rad
                TargetResolutionHeight = 100, # number of pixels in x
                TargetResolutionWidth = 100, # number of pixels in y
                TargetMillisecondsPerPixel = 10.2) as afm: # integration time, in ms
        afm.scan()
        afm.wait_for_scan() # omit to do something while scan is running
        uuid = afm.uuid # use uuid to identify scan results in database
        return afm.data

def scan_nanoftir():
    with scan.Fourier(LaserSourceTargetWavelength= 2000, # corresponds to range E of nanoFTIR laser
                      Name = "nanoFTIR spectrum", # name displayed in project browser
                      PhysicalOffsetX = 50, # central position in x, in um
                      PhysicalOffsetY = 50, # central position in y, in um
                      PhysicalRangeM = (0,800) # start and stop of nanoFTIR stage, in um
                      ResolutionDepth = 1024 # pixel in spectrum
                      TargetMillisecondsPerPixel = 10.2) as fourier: # integration time
        fourier.scan()
        fourier.wait_for_scan()
        interferograms = fourier.data
        spectra = fourier.spectra
        return spectra
