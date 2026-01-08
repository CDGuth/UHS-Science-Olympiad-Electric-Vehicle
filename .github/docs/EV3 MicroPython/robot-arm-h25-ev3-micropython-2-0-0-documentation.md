# Robot Arm H25[¶](#robot-arm-h25 "Permalink to this headline")

This example program makes Robot Arm H25 move the black wheel hub stacks around forever. The robot arm will first initialize and then start moving the hubs around.

Building instructions

Click [here](https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core) to find all building instructions for the Core Set Models, or use [this link](https://le-www-live-s.legocdn.com/sc/media/lessons/mindstorms-ev3/building-instructions/ev3-model-core-set-robot-arm-h25-56cdb22c1e3a02f1770bda72862ce2bd.pdf) to go to Robot Arm H25 directly.

Tip

When building the robot, reverse the orientation of the EV3 Brick such that the microSD card is easily accessible.

![../_images/robot_arm.jpg](../_images/robot_arm.jpg)

Figure 28 Robot Arm H25

Example program

#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Robot Arm Program
\-----------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait

\# Initialize the EV3 Brick
ev3 \= EV3Brick()

\# Configure the gripper motor on Port A with default settings.
gripper\_motor \= Motor(Port.A)

\# Configure the elbow motor. It has an 8-teeth and a 40-teeth gear
\# connected to it. We would like positive speed values to make the
\# arm go upward. This corresponds to counterclockwise rotation
\# of the motor.
elbow\_motor \= Motor(Port.B, Direction.COUNTERCLOCKWISE, \[8, 40\])

\# Configure the motor that rotates the base. It has a 12-teeth and a
\# 36-teeth gear connected to it. We would like positive speed values
\# to make the arm go away from the Touch Sensor. This corresponds
\# to counterclockwise rotation of the motor.
base\_motor \= Motor(Port.C, Direction.COUNTERCLOCKWISE, \[12, 36\])

\# Limit the elbow and base accelerations. This results in
\# very smooth motion. Like an industrial robot.
elbow\_motor.control.limits(speed\=60, acceleration\=120)
base\_motor.control.limits(speed\=60, acceleration\=120)

\# Set up the Touch Sensor. It acts as an end-switch in the base
\# of the robot arm. It defines the starting point of the base.
base\_switch \= TouchSensor(Port.S1)

\# Set up the Color Sensor. This sensor detects when the elbow
\# is in the starting position. This is when the sensor sees the
\# white beam up close.
elbow\_sensor \= ColorSensor(Port.S3)

\# Initialize the elbow. First make it go down for one second.
\# Then make it go upwards slowly (15 degrees per second) until
\# the Color Sensor detects the white beam. Then reset the motor
\# angle to make this the zero point. Finally, hold the motor
\# in place so it does not move.
elbow\_motor.run\_time(\-30, 1000)
elbow\_motor.run(15)
while elbow\_sensor.reflection() < 32:
    wait(10)
elbow\_motor.reset\_angle(0)
elbow\_motor.hold()

\# Initialize the base. First rotate it until the Touch Sensor
\# in the base is pressed. Reset the motor angle to make this
\# the zero point. Then hold the motor in place so it does not move.
base\_motor.run(\-60)
while not base\_switch.pressed():
    wait(10)
base\_motor.reset\_angle(0)
base\_motor.hold()

\# Initialize the gripper. First rotate the motor until it stalls.
\# Stalling means that it cannot move any further. This position
\# corresponds to the closed position. Then rotate the motor
\# by 90 degrees such that the gripper is open.
gripper\_motor.run\_until\_stalled(200, then\=Stop.COAST, duty\_limit\=50)
gripper\_motor.reset\_angle(0)
gripper\_motor.run\_target(200, \-90)

def robot\_pick(position):
    \# This function makes the robot base rotate to the indicated
    \# position. There it lowers the elbow, closes the gripper, and
    \# raises the elbow to pick up the object.

    \# Rotate to the pick-up position.
    base\_motor.run\_target(60, position)
    \# Lower the arm.
    elbow\_motor.run\_target(60, \-40)
    \# Close the gripper to grab the wheel stack.
    gripper\_motor.run\_until\_stalled(200, then\=Stop.HOLD, duty\_limit\=50)
    \# Raise the arm to lift the wheel stack.
    elbow\_motor.run\_target(60, 0)

def robot\_release(position):
    \# This function makes the robot base rotate to the indicated
    \# position. There it lowers the elbow, opens the gripper to
    \# release the object. Then it raises its arm again.

    \# Rotate to the drop-off position.
    base\_motor.run\_target(60, position)
    \# Lower the arm to put the wheel stack on the ground.
    elbow\_motor.run\_target(60, \-40)
    \# Open the gripper to release the wheel stack.
    gripper\_motor.run\_target(200, \-90)
    \# Raise the arm.
    elbow\_motor.run\_target(60, 0)

\# Play three beeps to indicate that the initialization is complete.
for i in range(3):
    ev3.speaker.beep()
    wait(100)

\# Define the three destinations for picking up and moving the wheel stacks.
LEFT \= 160
MIDDLE \= 100
RIGHT \= 40

\# This is the main part of the program. It is a loop that repeats endlessly.
#
\# First, the robot moves the object on the left towards the middle.
\# Second, the robot moves the object on the right towards the left.
\# Finally, the robot moves the object that is now in the middle, to the right.
#
\# Now we have a wheel stack on the left and on the right as before, but they
\# have switched places. Then the loop repeats to do this over and over.
while True:
    \# Move a wheel stack from the left to the middle.
    robot\_pick(LEFT)
    robot\_release(MIDDLE)

    \# Move a wheel stack from the right to the left.
    robot\_pick(RIGHT)
    robot\_release(LEFT)

    \# Move a wheel stack from the middle to the right.
    robot\_pick(MIDDLE)
    robot\_release(RIGHT)