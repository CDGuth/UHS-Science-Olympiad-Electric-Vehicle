# Line Following[¶](#line-following "Permalink to this headline")

This example project shows how you can make a robotic vehicle track a line using the [`ColorSensor`](../ev3devices.html#pybricks.ev3devices.ColorSensor "pybricks.ev3devices.ColorSensor") and the [`DriveBase`](../robotics.html#pybricks.robotics.DriveBase "pybricks.robotics.DriveBase") class. This works by adjusting the turn rate based on how much the measured reflection deviates from the threshold value. The threshold value is selected as the average of the line reflection and the reflection of the surrounding surface.

Building instructions

Click [here](https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#robot) to find all building instructions for the Educator Bot, or use [this link](https://le-www-live-s.legocdn.com/sc/media/lessons/mindstorms-ev3/building-instructions/ev3-rem-color-sensor-down-driving-base-d30ed30610c3d6647d56e17bc64cf6e2.pdf) to go to the color sensor attachment directly.

![../_images/robot_educator_line.jpg](../_images/robot_educator_line.jpg)

Figure 25 Robot Educator with the Color Sensor

Example program

This example uses the track shown in [Figure 26](#fig-map), but you can adapt this example to follow other lines as well. Download the line following track using the link below and print print the required pages. You can also create your own track by printing other pages.

[`Click to download the line following track.`](../_downloads/linefollowtiles.pdf)

![../_images/line.png](../_images/line.png)

Figure 26 Download the line following track and print pages `2,2,2,2,3,3,3,3,11`.

#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Robot Educator Color Sensor Down Program
\----------------------------------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#robot
"""

from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase

\# Initialize the motors.
left\_motor \= Motor(Port.B)
right\_motor \= Motor(Port.C)

\# Initialize the color sensor.
line\_sensor \= ColorSensor(Port.S3)

\# Initialize the drive base.
robot \= DriveBase(left\_motor, right\_motor, wheel\_diameter\=55.5, axle\_track\=104)

\# Calculate the light threshold. Choose values based on your measurements.
BLACK \= 9
WHITE \= 85
threshold \= (BLACK + WHITE) / 2

\# Set the drive speed at 100 millimeters per second.
DRIVE\_SPEED \= 100

\# Set the gain of the proportional line controller. This means that for every
\# percentage point of light deviating from the threshold, we set the turn
\# rate of the drivebase to 1.2 degrees per second.

\# For example, if the light value deviates from the threshold by 10, the robot
\# steers at 10\*1.2 = 12 degrees per second.
PROPORTIONAL\_GAIN \= 1.2

\# Start following the line endlessly.
while True:
    \# Calculate the deviation from the threshold.
    deviation \= line\_sensor.reflection() \- threshold

    \# Calculate the turn rate.
    turn\_rate \= PROPORTIONAL\_GAIN \* deviation

    \# Set the drive base speed and turn rate.
    robot.drive(DRIVE\_SPEED, turn\_rate)

    \# You can wait for a short time or do other things in this loop.
    wait(10)