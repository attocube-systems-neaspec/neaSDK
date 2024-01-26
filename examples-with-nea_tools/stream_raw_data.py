from time import sleep
import numpy as np
import matplotlib.pyplot as plt

from nea_tools.microscope.stream import AnalogDumpStream

num_samples = 8192
signals = ['Mechanical','Optical']


spectrum_mechanical = None

def callback(array):
    spectrum_x = np.linspace(0,num_samples//2*adstream.sample_resolution,num_samples//2)
    spectrum_y = np.absolute(np.fft.rfft(array[0]))    
    # max amplitude of non DC component
    index = np.argmax(spectrum_y[1:])
    # should be m1a
    print(spectrum_x[index],spectrum_y[index])
    

with AnalogDumpStream(buffersize=num_samples,signals=signals,callback=callback) as adstream:
    for i in range(10):
        adstream.run_single_iteration()
        sleep(1)



