# Obstacle Avoidance[¶](#obstacle-avoidance "Permalink to this headline")

This example project shows how you can make a robotic vehicle respond to its environment using sensors. The robot drives at a given speed until it detects an obstacle with the [`UltrasonicSensor`](../ev3devices.html#pybricks.ev3devices.UltrasonicSensor "pybricks.ev3devices.UltrasonicSensor"). Then the robot backs up, turns around, and continues driving until it detects a new obstacle.

Building instructions

Click [here](https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#robot) to find all building instructions for the Educator Bot, or use [this link](https://le-www-live-s.legocdn.com/sc/media/lessons/mindstorms-ev3/building-instructions/ev3-ultrasonic-sensor-driving-base-61ffdfa461aee2470b8ddbeab16e2070.pdf) to go to the ultrasonic sensor attachment directly.

![../_images/robot_educator_ultrasonic.jpg](../_images/robot_educator_ultrasonic.jpg)

Figure 24 Robot Educator with the Ultrasonic Sensor

Example program

#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Robot Educator Ultrasonic Sensor Driving Base Program
\-----------------------------------------------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#robot
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase

\# Initialize the EV3 Brick.
ev3 \= EV3Brick()

\# Initialize the Ultrasonic Sensor. It is used to detect
\# obstacles as the robot drives around.
obstacle\_sensor \= UltrasonicSensor(Port.S4)

\# Initialize two motors with default settings on Port B and Port C.
\# These will be the left and right motors of the drive base.
left\_motor \= Motor(Port.B)
right\_motor \= Motor(Port.C)

\# The DriveBase is composed of two motors, with a wheel on each motor.
\# The wheel\_diameter and axle\_track values are used to make the motors
\# move at the correct speed when you give a motor command.
\# The axle track is the distance between the points where the wheels
\# touch the ground.
robot \= DriveBase(left\_motor, right\_motor, wheel\_diameter\=55.5, axle\_track\=104)

\# Play a sound to tell us when we are ready to start moving
ev3.speaker.beep()

\# The following loop makes the robot drive forward until it detects an
\# obstacle. Then it backs up and turns around. It keeps on doing this
\# until you stop the program.
while True:
    \# Begin driving forward at 200 millimeters per second.
    robot.drive(200, 0)

    \# Wait until an obstacle is detected. This is done by repeatedly
    \# doing nothing (waiting for 10 milliseconds) while the measured
    \# distance is still greater than 300 mm.
    while obstacle\_sensor.distance() \> 300:
        wait(10)

    \# Drive backward for 300 millimeters.
    robot.straight(\-300)

    \# Turn around by 120 degrees
    robot.turn(120)