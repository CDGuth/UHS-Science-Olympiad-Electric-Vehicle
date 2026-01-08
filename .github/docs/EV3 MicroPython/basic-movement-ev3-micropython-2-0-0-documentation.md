# Basic Movement[¶](#basic-movement "Permalink to this headline")

This example project shows how you can make a robotic vehicle drive for a given distance or turn by a given angle. Check out the [`DriveBase`](../robotics.html#pybricks.robotics.DriveBase "pybricks.robotics.DriveBase") class for tips and tricks for precise movements.

Building instructions

Click [here](https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#robot) to find all building instructions for the Educator Bot, or use [this link](https://le-www-live-s.legocdn.com/sc/media/lessons/mindstorms-ev3/building-instructions/ev3-rem-driving-base-79bebfc16bd491186ea9c9069842155e.pdf) to go to the driving base directly.

![../_images/robot_educator_basic.jpg](../_images/robot_educator_basic.jpg)

Figure 23 Robot Educator

Example program

#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Robot Educator Driving Base Program
\-----------------------------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#robot
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

\# Initialize the EV3 Brick.
ev3 \= EV3Brick()

\# Initialize the motors.
left\_motor \= Motor(Port.B)
right\_motor \= Motor(Port.C)

\# Initialize the drive base.
robot \= DriveBase(left\_motor, right\_motor, wheel\_diameter\=55.5, axle\_track\=104)

\# Go forward and backwards for one meter.
robot.straight(1000)
ev3.speaker.beep()

robot.straight(\-1000)
ev3.speaker.beep()

\# Turn clockwise by 360 degrees and back again.
robot.turn(360)
ev3.speaker.beep()

robot.turn(\-360)
ev3.speaker.beep()