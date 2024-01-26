"""
Collection of standard commands like sweeping the resonance frequency,
aligning the mechanical detection, setting some parameters, and
approaching the sample.
"""

from neaspec import context
from nea_tools.logic import *
from nea_tools.microscope import dds, pilot, regulator

# assuming tip is located under deflection laser
# and sample is close to tip

# full range sweep
with Sweep(10000, 500000) as rough_sweep:
    rough_sweep.await_sweep()
    rough_freq = rough_sweep.res_frequ

with Sweep(rough_freq-2000,rough_freq+2000) as fine_sweep:
    fine_sweep.await_sweep()

context.Logic.AdjustResonantFrequencyDownToAmplitude.Execute(0.9)

context.Logic.AutoAlignEdgeForMaximalM1A.Execute()

# increase/decrease tapping amplitude by 10 mV
dds.head.amplitude += 10 
dds.head.amplitude -= 10

# approach slowly by reducing regulator value
old_reg_i = regulator.i
regulator.i = -0.2

with Approach(setpoint = 0.8) as approach:
    approach.await_approach()

regulator.i = old_reg_i

# turn on pilot
pilot.enable()
