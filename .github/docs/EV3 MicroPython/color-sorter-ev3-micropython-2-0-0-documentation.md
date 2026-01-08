# Color Sorter[¶](#color-sorter "Permalink to this headline")

This example project makes the Color Sorter scan colored Technic beams using the [`ColorSensor`](../ev3devices.html#pybricks.ev3devices.ColorSensor "pybricks.ev3devices.ColorSensor").

Scan the colored beams one by one and add them to the tray. A beep confirms that it has registered the color. When the tray is full or when you press the center button, the robot will start distributing the Technic bricks by color.

Building instructions

Click [here](https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core) to find all building instructions for the Core Set Models, or use [this link](https://le-www-live-s.legocdn.com/sc/media/lessons/mindstorms-ev3/building-instructions/ev3-model-core-set-color-sorter-c778563f88c986841453574495cb5ff1.pdf) to go to the Color Sorter directly.

![../_images/color_sorter.jpg](../_images/color_sorter.jpg)

Figure 27 Color Sorter

Example program

#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Color Sorter Program
\--------------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile
from pybricks.tools import wait

\# The colored objects are either red, green, blue, or yellow.
POSSIBLE\_COLORS \= \[Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW\]

\# Initialize the EV3 brick.
ev3 \= EV3Brick()

\# Initialize the motors that drive the conveyor belt and eject the objects.
belt\_motor \= Motor(Port.D)
feed\_motor \= Motor(Port.A)

\# Initialize the Touch Sensor. It is used to detect when the belt motor has
\# moved the sorter module all the way to the left.
touch\_sensor \= TouchSensor(Port.S1)

\# Initialize the Color Sensor. It is used to detect the color of the objects.
color\_sensor \= ColorSensor(Port.S3)

\# This is the main loop. It waits for you to scan and insert 8 colored objects.
\# Then it sorts them by color. Then the process starts over and you can scan
\# and insert the next set of colored objects.
while True:
    \# Get the feed motor in the correct starting position.
    \# This is done by running the motor forward until it stalls. This
    \# means that it cannot move any further. From this end point, the motor
    \# rotates backward by 180 degrees. Then it is in the starting position.
    feed\_motor.run\_until\_stalled(120, duty\_limit\=50)
    feed\_motor.run\_angle(450, \-200)

    \# Get the conveyor belt motor in the correct starting position.
    \# This is done by first running the belt motor backward until the
    \# touch sensor becomes pressed. Then the motor stops, and the the angle is
    \# reset to zero. This means that when it rotates backward to zero later
    \# on, it returns to this starting position.
    belt\_motor.run(\-500)
    while not touch\_sensor.pressed():
        pass
    belt\_motor.stop()
    wait(1000)
    belt\_motor.reset\_angle(0)

    \# When we scan the objects, we store all the color numbers in a list.
    \# We start with an empty list. It will grow as we add colors to it.
    color\_list \= \[\]

    \# This loop scans the colors of the objects. It repeats until 8 objects
    \# are scanned and placed in the chute. This is done by repeating the loop
    \# while the length of the list is still less than 8.
    while len(color\_list) < 8:
        \# Show an arrow that points to the color sensor.
        ev3.screen.load\_image(ImageFile.RIGHT)

        \# Show how many colored objects we have already scanned.
        ev3.screen.print(len(color\_list))

        \# Wait for the center button to be pressed or a color to be scanned.
        while True:
            \# Store True if the center button is pressed or False if not.
            pressed \= Button.CENTER in ev3.buttons.pressed()
            \# Store the color measured by the Color Sensor.
            color \= color\_sensor.color()
            \# If the center button is pressed or a color is detected,
            \# break out of the loop.
            if pressed or color in POSSIBLE\_COLORS:
                break

        if pressed:
            \# If the button was pressed, end the loop early. We will no longer
            \# wait for any remaining objects to be scanned and added to the
            \# chute.
            break

        \# Otherwise, a color was scanned. So we add (append) it to the list.
        ev3.speaker.beep(1000, 100)
        color\_list.append(color)

        \# We don't want to register the same color once more if we're still
        \# looking at the same object. So before we continue, we wait until the
        \# sensor no longer sees the object.
        while color\_sensor.color() in POSSIBLE\_COLORS:
            pass
        ev3.speaker.beep(2000, 100)

        \# Show an arrow pointing to the center button, to ask if we are done.
        ev3.screen.load\_image(ImageFile.BACKWARD)
        wait(2000)

    \# Play a sound and show an image to indicate that we are done scanning.
    ev3.speaker.play\_file(SoundFile.READY)
    ev3.screen.load\_image(ImageFile.EV3)

    \# Now sort the bricks according the list of colors that we stored.
    \# We do this by going over each color in the list in a loop.
    for color in color\_list:
        \# Wait for one second between each sorting action.
        wait(1000)

        \# Run the conveyor belt motor to the right position based on the color.
        if color \== Color.BLUE:
            ev3.speaker.say('blue')
            belt\_motor.run\_target(500, 10)
        elif color \== Color.GREEN:
            ev3.speaker.say('green')
            belt\_motor.run\_target(500, 132)
        elif color \== Color.YELLOW:
            ev3.speaker.say('yellow')
            belt\_motor.run\_target(500, 360)
        elif color \== Color.RED:
            ev3.speaker.say('red')
            belt\_motor.run\_target(500, 530)

        \# Now that the conveyor belt is in the correct position, eject the
        \# colored object.
        feed\_motor.run\_angle(1500, 180)
        feed\_motor.run\_angle(1500, \-180)