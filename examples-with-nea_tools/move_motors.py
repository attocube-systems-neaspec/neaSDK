"""
Moving the sample and mirror positioniers. 
"""

from nea_tools.microscope import motors

with motors.Sample() as sample:
    sample.activate()
    sample.move(vx=0, vy=0, vz=-0.001)  # moving down
    sample.await_movement()
    sample.move(vx=0, vy=0, vz=0.001, dt=0.1)  # moving up
    sample.await_movement()

mirror = motors.Mirror()
mirror.activate()
mirror.go_relative(250,0,0)
mirror.await_movement()
mirror.deactivate()
