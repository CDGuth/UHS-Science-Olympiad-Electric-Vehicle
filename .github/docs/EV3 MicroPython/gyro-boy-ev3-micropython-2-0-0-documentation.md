# Gyro Boy[¶](#gyro-boy "Permalink to this headline")

This program makes Gyro Boy balance on its two wheels using the [`GyroSensor`](../ev3devices.html#pybricks.ev3devices.GyroSensor "pybricks.ev3devices.GyroSensor"). The duty cycle of the motors is continuously adjusted as a function of the gyro angle, the gyro speed, the motor angles, and the motor speeds, in order to maintain balance.

This program also uses a Python generator function (a function that uses yield instead of return) as a coroutine. Coroutines are a form of cooperative multitasking that allows the robot perform multiple tasks at the same time. This lets you drive it around while it is busy balancing.

Building instructions

Click [here](https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core) to find all building instructions for the Core Set Models, or use [this link](https://le-www-live-s.legocdn.com/sc/media/lessons/mindstorms-ev3/building-instructions/ev3-model-core-set-gyro-boy-f8a14d8e3d0e63fa23b87f798bf197f4.pdf) to go to Gyro Boy directly.

![../_images/gyro_boy.jpg](../_images/gyro_boy.jpg)

Figure 30 Gyro Boy

Example program

#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Gyro Boy Program
\----------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core
"""

from ucollections import namedtuple
import urandom

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, ColorSensor, GyroSensor
from pybricks.parameters import Port, Color, ImageFile, SoundFile
from pybricks.tools import wait, StopWatch

\# Initialize the EV3 brick.
ev3 \= EV3Brick()

\# Initialize the motors connected to the drive wheels.
left\_motor \= Motor(Port.D)
right\_motor \= Motor(Port.A)

\# Initialize the motor connected to the arms.
arm\_motor \= Motor(Port.C)

\# Initialize the Color Sensor. It is used to detect the colors that command
\# which way the robot should move.
color\_sensor \= ColorSensor(Port.S1)

\# Initialize the gyro sensor. It is used to provide feedback for balancing the
\# robot.
gyro\_sensor \= GyroSensor(Port.S2)

\# Initialize the ultrasonic sensor. It is used to detect when the robot gets
\# too close to an obstruction.
ultrasonic\_sensor \= UltrasonicSensor(Port.S4)

\# Initialize the timers.
fall\_timer \= StopWatch()
single\_loop\_timer \= StopWatch()
control\_loop\_timer \= StopWatch()
action\_timer \= StopWatch()

\# The following (UPPERCASE names) are constants that control how the program
\# behaves.

GYRO\_CALIBRATION\_LOOP\_COUNT \= 200
GYRO\_OFFSET\_FACTOR \= 0.0005
TARGET\_LOOP\_PERIOD \= 15  \# ms
ARM\_MOTOR\_SPEED \= 600  \# deg/s

\# Actions will be used to change which way the robot drives.
Action \= namedtuple('Action ', \['drive\_speed', 'steering'\])

\# These are the pre-defined actions
STOP \= Action(drive\_speed\=0, steering\=0)
FORWARD\_FAST \= Action(drive\_speed\=150, steering\=0)
FORWARD\_SLOW \= Action(drive\_speed\=40, steering\=0)
BACKWARD\_FAST \= Action(drive\_speed\=-75, steering\=0)
BACKWARD\_SLOW \= Action(drive\_speed\=-10, steering\=0)
TURN\_RIGHT \= Action(drive\_speed\=0, steering\=70)
TURN\_LEFT \= Action(drive\_speed\=0, steering\=-70)

\# The colors that the color sensor can detect are mapped to actions that the
\# robot can perform.
ACTION\_MAP \= {
    Color.RED: STOP,
    Color.GREEN: FORWARD\_FAST,
    Color.BLUE: TURN\_RIGHT,
    Color.YELLOW: TURN\_LEFT,
    Color.WHITE: BACKWARD\_FAST,
}

\# This function monitors the color sensor and ultrasonic sensor.
#
\# It is important that no blocking calls are made in this function, otherwise
\# it will affect the control loop time in the main program. Instead, we yield
\# to the control loop while we are waiting for a certain thing to happen like
\# this:
#
\#     while not condition:
\#         yield
#
\# We also use yield to update the drive speed and steering values in the main
\# control loop:
#
\#     yield action
#
def update\_action():
    arm\_motor.reset\_angle(0)
    action\_timer.reset()

    \# Drive forward for 4 seconds to leave stand, then stop.
    yield FORWARD\_SLOW
    while action\_timer.time() < 4000:
        yield

    action \= STOP
    yield action

    \# Start checking sensors on arms. When specific conditions are sensed,
    \# different actions will be performed.
    while True:
        \# First, we check the color sensor. The detected color is looked up in
        \# the action map.
        new\_action \= ACTION\_MAP.get(color\_sensor.color())

        \# If the color was found, beep for 0.1 seconds and then change the
        \# action depending on which color was detected.
        if new\_action is not None:
            action\_timer.reset()
            ev3.speaker.beep(1000, \-1)
            while action\_timer.time() < 100:
                yield
            ev3.speaker.beep(0, \-1)

            \# If the new action involves steering, combine the new steering
            \# with the old drive speed. Otherwise, use the entire new action.
            if new\_action.steering != 0:
                action \= Action(drive\_speed\=action.drive\_speed,
                                steering\=new\_action.steering)
            else:
                action \= new\_action
            yield action

        \# If the measured distance of the ultrasonic sensor is less than 250
        \# millimeters, then back up slowly.
        if ultrasonic\_sensor.distance() < 250:
            \# Back up slowly while wiggling the arms back and forth.
            yield BACKWARD\_SLOW

            arm\_motor.run\_angle(ARM\_MOTOR\_SPEED, 30, wait\=False)
            while not arm\_motor.control.done():
                yield
            arm\_motor.run\_angle(ARM\_MOTOR\_SPEED, \-60, wait\=False)
            while not arm\_motor.control.done():
                yield
            arm\_motor.run\_angle(ARM\_MOTOR\_SPEED, 30, wait\=False)
            while not arm\_motor.control.done():
                yield

            \# Randomly turn left or right for 4 seconds while still backing
            \# up slowly.
            turn \= urandom.choice(\[TURN\_LEFT, TURN\_RIGHT\])
            yield Action(drive\_speed\=BACKWARD\_SLOW.drive\_speed,
                         steering\=turn.steering)
            action\_timer.reset()
            while action\_timer.time() < 4000:
                yield

            \# Beep and then restore the previous action from before the
            \# ultrasonic sensor detected an obstruction.
            action\_timer.reset()
            ev3.speaker.beep(1000, \-1)
            while action\_timer.time() < 100:
                yield
            ev3.speaker.beep(0, \-1)

            yield action

        \# This adds a small delay since we don't need to read these sensors
        \# continuously. Reading once every 100 milliseconds is fast enough.
        action\_timer.reset()
        while action\_timer.time() < 100:
            yield

\# If we fall over in the middle of an action, the arm motors could be moving or
\# the speaker could be beeping, so we need to stop both of those.
def stop\_action():
    ev3.speaker.beep(0, \-1)
    arm\_motor.run\_target(ARM\_MOTOR\_SPEED, 0)

while True:
    \# Sleeping eyes and light off let us know that the robot is waiting for
    \# any movement to stop before the program can continue.
    ev3.screen.load\_image(ImageFile.SLEEPING)
    ev3.light.off()

    \# Reset the sensors and variables.
    left\_motor.reset\_angle(0)
    right\_motor.reset\_angle(0)
    fall\_timer.reset()

    motor\_position\_sum \= 0
    wheel\_angle \= 0
    motor\_position\_change \= \[0, 0, 0, 0\]
    drive\_speed, steering \= 0, 0
    control\_loop\_count \= 0
    robot\_body\_angle \= \-0.25

    \# Since update\_action() is a generator (it uses "yield" instead of
    \# "return") this doesn't actually run update\_action() right now but
    \# rather prepares it for use later.
    action\_task \= update\_action()

    \# Calibrate the gyro offset. This makes sure that the robot is perfectly
    \# still by making sure that the measured rate does not fluctuate more than
    \# 2 deg/s. Gyro drift can cause the rate to be non-zero even when the robot
    \# is not moving, so we save that value for use later.
    while True:
        gyro\_minimum\_rate, gyro\_maximum\_rate \= 440, \-440
        gyro\_sum \= 0
        for \_ in range(GYRO\_CALIBRATION\_LOOP\_COUNT):
            gyro\_sensor\_value \= gyro\_sensor.speed()
            gyro\_sum += gyro\_sensor\_value
            if gyro\_sensor\_value \> gyro\_maximum\_rate:
                gyro\_maximum\_rate \= gyro\_sensor\_value
            if gyro\_sensor\_value < gyro\_minimum\_rate:
                gyro\_minimum\_rate \= gyro\_sensor\_value
            wait(5)
        if gyro\_maximum\_rate \- gyro\_minimum\_rate < 2:
            break
    gyro\_offset \= gyro\_sum / GYRO\_CALIBRATION\_LOOP\_COUNT

    \# Awake eyes and green light let us know that the robot is ready to go!
    ev3.speaker.play\_file(SoundFile.SPEED\_UP)
    ev3.screen.load\_image(ImageFile.AWAKE)
    ev3.light.on(Color.GREEN)

    \# Main control loop for balancing the robot.
    while True:
        \# This timer measures how long a single loop takes. This will be used
        \# to help keep the loop time consistent, even when different actions
        \# are happening.
        single\_loop\_timer.reset()

        \# This calculates the average control loop period. This is used in the
        \# control feedback calculation instead of the single loop time to
        \# filter out random fluctuations.
        if control\_loop\_count \== 0:
            \# The first time through the loop, we need to assign a value to
            \# avoid dividing by zero later.
            average\_control\_loop\_period \= TARGET\_LOOP\_PERIOD / 1000
            control\_loop\_timer.reset()
        else:
            average\_control\_loop\_period \= (control\_loop\_timer.time() / 1000 /
                                           control\_loop\_count)
        control\_loop\_count += 1

        \# calculate robot body angle and speed
        gyro\_sensor\_value \= gyro\_sensor.speed()
        gyro\_offset \*= (1 \- GYRO\_OFFSET\_FACTOR)
        gyro\_offset += GYRO\_OFFSET\_FACTOR \* gyro\_sensor\_value
        robot\_body\_rate \= gyro\_sensor\_value \- gyro\_offset
        robot\_body\_angle += robot\_body\_rate \* average\_control\_loop\_period

        \# calculate wheel angle and speed
        left\_motor\_angle \= left\_motor.angle()
        right\_motor\_angle \= right\_motor.angle()
        previous\_motor\_sum \= motor\_position\_sum
        motor\_position\_sum \= left\_motor\_angle + right\_motor\_angle
        change \= motor\_position\_sum \- previous\_motor\_sum
        motor\_position\_change.insert(0, change)
        del motor\_position\_change\[\-1\]
        wheel\_angle += change \- drive\_speed \* average\_control\_loop\_period
        wheel\_rate \= sum(motor\_position\_change) / 4 / average\_control\_loop\_period

        \# This is the main control feedback calculation.
        output\_power \= (\-0.01 \* drive\_speed) + (0.8 \* robot\_body\_rate +
                                                15 \* robot\_body\_angle +
                                                0.08 \* wheel\_rate +
                                                0.12 \* wheel\_angle)
        if output\_power \> 100:
            output\_power \= 100
        if output\_power < \-100:
            output\_power \= \-100

        \# Drive the motors.
        left\_motor.dc(output\_power \- 0.1 \* steering)
        right\_motor.dc(output\_power + 0.1 \* steering)

        \# Check if robot fell down. If the output speed is +/-100% for more
        \# than one second, we know that we are no longer balancing properly.
        if abs(output\_power) < 100:
            fall\_timer.reset()
        elif fall\_timer.time() \> 1000:
            break

        \# This runs update\_action() until the next "yield" statement.
        action \= next(action\_task)
        if action is not None:
            drive\_speed, steering \= action

        \# Make sure loop time is at least TARGET\_LOOP\_PERIOD. The output power
        \# calculation above depends on having a certain amount of time in each
        \# loop.
        wait(TARGET\_LOOP\_PERIOD \- single\_loop\_timer.time())

    \# Handle falling over. If we get to this point in the program, it means
    \# that the robot fell over.

    \# Stop all of the motors.
    stop\_action()
    left\_motor.stop()
    right\_motor.stop()

    \# Knocked out eyes and red light let us know that the robot lost its
    \# balance.
    ev3.light.on(Color.RED)
    ev3.screen.load\_image(ImageFile.KNOCKED\_OUT)
    ev3.speaker.play\_file(SoundFile.SPEED\_DOWN)

    \# Wait for a few seconds before trying to balance again.
    wait(3000)