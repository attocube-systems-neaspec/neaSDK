"""
Moves tip to given xy coordinates one after another with given speed.
"""
from neaspec import context
import Nea.Client.SharedDefinitions as nea
from time import sleep

# coordinates in µm
xy_coords = [
    (49,50),
    (49,49),
    (50,49),
    (50,50),
]
speed = 0.2 # µm/s
do_wait = False


def on_tip_position_moved(sender, args):
    print(f"Arrived at {args.Point}\n")
    global do_wait
    do_wait = False

def on_tip_position_moving(sender, args):
    print(f"Moving to {args.Point}\n")
    global do_wait
    do_wait = True

context.Logic.TipPositionMoved += on_tip_position_moved
context.Logic.TipPositionMoving += on_tip_position_moving

for coord in xy_coords:
    args = nea.MoveTipPositionArgs(nea.Geometry.Point2D(*coord), speed/1000)
    context.Logic.MoveTipPosition.Execute(args)
    sleep(0.1)
    while do_wait:
        sleep(0.1)
    sleep(0.2)

context.Logic.TipPositionMoved -= on_tip_position_moved
context.Logic.TipPositionMoving -= on_tip_position_moving
