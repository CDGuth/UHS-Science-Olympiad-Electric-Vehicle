# Puppy[¶](#puppy "Permalink to this headline")

This example program gives the Puppy up to 8 behaviors. It exhibits different behaviors in response to being fed (the [`ColorSensor`](../ev3devices.html#pybricks.ev3devices.ColorSensor "pybricks.ev3devices.ColorSensor") sees colors) or petted (the [`TouchSensor`](../ev3devices.html#pybricks.ev3devices.TouchSensor "pybricks.ev3devices.TouchSensor") is pressed).

Building instructions

Click [here](https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core) to find all building instructions for the Core Set Models, or use [this link](https://le-www-live-s.legocdn.com/sc/media/lessons/mindstorms-ev3/building-instructions/ev3-model-core-set-puppy-7a316ae71b8ecdcd72ad4c4bcd15845d.pdf) to go to the Puppy directly.

![../_images/puppy.jpg](../_images/puppy.jpg)

Figure 29 Puppy

Example program

#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Puppy Program
\-------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core
"""

import urandom

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Button, Color, Direction
from pybricks.media.ev3dev import Image, ImageFile, SoundFile
from pybricks.tools import wait, StopWatch

class Puppy:
    \# These constants are used for positioning the legs.
    HALF\_UP\_ANGLE \= 25
    STAND\_UP\_ANGLE \= 65
    STRETCH\_ANGLE \= 125

    \# These constants are for positioning the head.
    HEAD\_UP\_ANGLE \= 0
    HEAD\_DOWN\_ANGLE \= \-40

    \# These constants are for the eyes.
    NEUTRAL\_EYES \= Image(ImageFile.NEUTRAL)
    TIRED\_EYES \= Image(ImageFile.TIRED\_MIDDLE)
    TIRED\_LEFT\_EYES \= Image(ImageFile.TIRED\_LEFT)
    TIRED\_RIGHT\_EYES \= Image(ImageFile.TIRED\_RIGHT)
    SLEEPING\_EYES \= Image(ImageFile.SLEEPING)
    HURT\_EYES \= Image(ImageFile.HURT)
    ANGRY\_EYES \= Image(ImageFile.ANGRY)
    HEART\_EYES \= Image(ImageFile.LOVE)
    SQUINTY\_EYES \= Image(ImageFile.TEAR)  \# the tear is erased later

    def \_\_init\_\_(self):
        \# Initialize the EV3 brick.
        self.ev3 \= EV3Brick()

        \# Initialize the motors connected to the back legs.
        self.left\_leg\_motor \= Motor(Port.D, Direction.COUNTERCLOCKWISE)
        self.right\_leg\_motor \= Motor(Port.A, Direction.COUNTERCLOCKWISE)

        \# Initialize the motor connected to the head.
        \# Worm gear moves 1 tooth per rotation. It is interfaced to a 24-tooth
        \# gear. The 24-tooth gear is connected to parallel 12-tooth gears via
        \# an axle. The 12-tooth gears interface with 36-tooth gears.
        self.head\_motor \= Motor(Port.C, Direction.COUNTERCLOCKWISE,
                                gears\=\[\[1, 24\], \[12, 36\]\])

        \# Initialize the Color Sensor. It is used to detect the colors when
        \# feeding the puppy.
        self.color\_sensor \= ColorSensor(Port.S4)

        \# Initialize the touch sensor. It is used to detect when someone pets
        \# the puppy.
        self.touch\_sensor \= TouchSensor(Port.S1)

        self.pet\_count\_timer \= StopWatch()
        self.feed\_count\_timer \= StopWatch()
        self.count\_changed\_timer \= StopWatch()

        \# These attributes are initialized later in the reset() method.
        self.pet\_target \= None
        self.feed\_target \= None
        self.pet\_count \= None
        self.feed\_count \= None

        \# These attributes are used by properties.
        self.\_behavior \= None
        self.\_behavior\_changed \= None
        self.\_eyes \= None
        self.\_eyes\_changed \= None

        \# These attributes are used in the eyes update
        self.eyes\_timer\_1 \= StopWatch()
        self.eyes\_timer\_1\_end \= 0
        self.eyes\_timer\_2 \= StopWatch()
        self.eyes\_timer\_2\_end \= 0
        self.eyes\_closed \= False

        \# These attributes are used by the playful behavior.
        self.playful\_timer \= StopWatch()
        self.playful\_bark\_interval \= None

        \# These attributes are used in the update methods.
        self.prev\_petted \= None
        self.prev\_color \= None

    def adjust\_head(self):
        """Use the up and down buttons on the EV3 brick to adjust the puppy's
        head up or down.
        """
        self.ev3.screen.load\_image(ImageFile.EV3\_ICON)
        self.ev3.light.on(Color.ORANGE)

        while True:
            buttons \= self.ev3.buttons.pressed()
            if Button.CENTER in buttons:
                break
            elif Button.UP in buttons:
                self.head\_motor.run(20)
            elif Button.DOWN in buttons:
                self.head\_motor.run(\-20)
            else:
                self.head\_motor.stop()
            wait(100)

        self.head\_motor.stop()
        self.head\_motor.reset\_angle(0)
        self.ev3.light.on(Color.GREEN)

    def move\_head(self, target):
        """Move the head to the target angle.

        Arguments:
            target (int):
                The target angle in degrees. 0 is the starting position,
                negative values are below this point and positive values
                are above this point.
        """
        self.head\_motor.run\_target(20, target)

    def reset(self):
        \# must be called when puppy is sitting down.
        self.left\_leg\_motor.reset\_angle(0)
        self.right\_leg\_motor.reset\_angle(0)
        \# Pick a random number of time to pet the puppy.
        self.pet\_target \= urandom.randint(3, 6)
        \# Pick a random number of time to feed the puppy.
        self.feed\_target \= urandom.randint(2, 4)
        \# Pet count and feed count both start at 1
        self.pet\_count, self.feed\_count \= 1, 1
        \# Reset timers.
        self.pet\_count\_timer.reset()
        self.feed\_count\_timer.reset()
        self.count\_changed\_timer.reset()
        \# Set initial behavior.
        self.behavior \= self.idle

    \# The next 8 methods define the 8 behaviors of the puppy.

    def idle(self):
        """The puppy is idle and waiting for someone to pet it or feed it."""
        if self.did\_behavior\_change:
            print('idle')
            self.stand\_up()
        self.update\_eyes()
        self.update\_behavior()
        self.update\_pet\_count()
        self.update\_feed\_count()

    def go\_to\_sleep(self):
        """Makes the puppy go to sleep."""
        if self.did\_behavior\_change:
            print('go\_to\_sleep')
            self.eyes \= self.TIRED\_EYES
            self.sit\_down()
            self.move\_head(self.HEAD\_DOWN\_ANGLE)
            self.eyes \= self.SLEEPING\_EYES
            self.ev3.speaker.play\_file(SoundFile.SNORING)
        if self.touch\_sensor.pressed() and Button.CENTER in self.ev3.buttons.pressed():
            self.count\_changed\_timer.reset()
            self.behavior \= self.wake\_up

    def wake\_up(self):
        """Makes the puppy wake up."""
        if self.did\_behavior\_change:
            print('wake\_up')
        self.eyes \= self.TIRED\_EYES
        self.ev3.speaker.play\_file(SoundFile.DOG\_WHINE)
        self.move\_head(self.HEAD\_UP\_ANGLE)
        self.sit\_down()
        self.stretch()
        wait(1000)
        self.stand\_up()
        self.behavior \= self.idle

    def act\_playful(self):
        """Makes the puppy act playful."""
        if self.did\_behavior\_change:
            print('act\_playful')
            self.eyes \= self.NEUTRAL\_EYES
            self.stand\_up()
            self.playful\_bark\_interval \= 0

        if self.update\_pet\_count():
            \# If the puppy was petted, then we are done being playful
            self.behavior \= self.idle

        if self.playful\_timer.time() \> self.playful\_bark\_interval:
            self.ev3.speaker.play\_file(SoundFile.DOG\_BARK\_2)
            self.playful\_timer.reset()
            self.playful\_bark\_interval \= urandom.randint(4, 8) \* 1000

    def act\_angry(self):
        """Makes the puppy act angry."""
        if self.did\_behavior\_change:
            print('act\_angry')
        self.eyes \= self.ANGRY\_EYES
        self.ev3.speaker.play\_file(SoundFile.DOG\_GROWL)
        self.stand\_up()
        wait(1500)
        self.ev3.speaker.play\_file(SoundFile.DOG\_BARK\_1)
        self.pet\_count \-= 1
        print('pet\_count:', self.pet\_count, 'pet\_target:', self.pet\_target)
        self.behavior \= self.idle

    def act\_hungry(self):
        if self.did\_behavior\_change:
            print('act\_hungry')
            self.eyes \= self.HURT\_EYES
            self.sit\_down()
            self.ev3.speaker.play\_file(SoundFile.DOG\_WHINE)

        if self.update\_feed\_count():
            \# If we got food, then we are not longer hungry.
            self.behavior \= self.idle

        if self.update\_pet\_count():
            \# If we got a pet instead of food, then we are angry.
            self.behavior \= self.act\_angry

    def go\_to\_bathroom(self):
        if self.did\_behavior\_change:
            print('go\_to\_bathroom')
        self.eyes \= self.SQUINTY\_EYES
        self.stand\_up()
        wait(100)
        self.right\_leg\_motor.run\_target(100, self.STRETCH\_ANGLE)
        wait(800)
        self.ev3.speaker.play\_file(SoundFile.HORN\_1)
        wait(1000)
        for \_ in range(3):
            self.right\_leg\_motor.run\_angle(100, 20)
            self.right\_leg\_motor.run\_angle(100, \-20)
        self.right\_leg\_motor.run\_target(100, self.STAND\_UP\_ANGLE)
        self.feed\_count \= 1
        self.behavior \= self.idle

    def act\_happy(self):
        if self.did\_behavior\_change:
            print('act\_happy')
        self.eyes \= self.HEART\_EYES
        \# self.move\_head(self.?)
        self.sit\_down()
        for \_ in range(3):
            self.ev3.speaker.play\_file(SoundFile.DOG\_BARK\_1)
            self.hop()
        wait(500)
        self.sit\_down()
        self.reset()

    def sit\_down(self):
        """Makes the puppy sit down."""
        self.left\_leg\_motor.run(\-50)
        self.right\_leg\_motor.run(\-50)
        wait(1000)
        self.left\_leg\_motor.stop()
        self.right\_leg\_motor.stop()
        wait(100)

    \# The next 4 methods define actions that are used to make some parts of
    \# the behaviors above.

    def stand\_up(self):
        """Makes the puppy stand up."""
        self.left\_leg\_motor.run\_target(100, self.HALF\_UP\_ANGLE, wait\=False)
        self.right\_leg\_motor.run\_target(100, self.HALF\_UP\_ANGLE)
        while not self.left\_leg\_motor.control.done():
            wait(100)

        self.left\_leg\_motor.run\_target(50, self.STAND\_UP\_ANGLE, wait\=False)
        self.right\_leg\_motor.run\_target(50, self.STAND\_UP\_ANGLE)
        while not self.left\_leg\_motor.control.done():
            wait(100)

        wait(500)

    def stretch(self):
        """Makes the puppy stretch its legs backwards."""
        self.stand\_up()

        self.left\_leg\_motor.run\_target(100, self.STRETCH\_ANGLE, wait\=False)
        self.right\_leg\_motor.run\_target(100, self.STRETCH\_ANGLE)
        while not self.left\_leg\_motor.control.done():
            wait(100)

        self.ev3.speaker.play\_file(SoundFile.DOG\_WHINE)

        self.left\_leg\_motor.run\_target(100, self.STAND\_UP\_ANGLE, wait\=False)
        self.right\_leg\_motor.run\_target(100, self.STAND\_UP\_ANGLE)
        while not self.left\_leg\_motor.control.done():
            wait(100)

    def hop(self):
        """Makes the puppy hop."""
        self.left\_leg\_motor.run(500)
        self.right\_leg\_motor.run(500)
        wait(275)
        self.left\_leg\_motor.hold()
        self.right\_leg\_motor.hold()
        wait(275)
        self.left\_leg\_motor.run(\-50)
        self.right\_leg\_motor.run(\-50)
        wait(275)
        self.left\_leg\_motor.stop()
        self.right\_leg\_motor.stop()

    @property
    def behavior(self):
        """Gets and sets the current behavior."""
        return self.\_behavior

    @behavior.setter
    def behavior(self, value):
        if self.\_behavior != value:
            self.\_behavior \= value
            self.\_behavior\_changed \= True

    @property
    def did\_behavior\_change(self):
        """bool: Tests if the behavior changed since the last time this
        property was read.
        """
        if self.\_behavior\_changed:
            self.\_behavior\_changed \= False
            return True
        return False

    def update\_behavior(self):
        """Updates the :prop:\`behavior\` property based on the current state
        of petting and feeding.
        """
        if self.pet\_count \== self.pet\_target and self.feed\_count \== self.feed\_target:
            \# If we have the exact right amount of pets and feeds, act happy.
            self.behavior \= self.act\_happy
        elif self.pet\_count \> self.pet\_target and self.feed\_count < self.feed\_target:
            \# If we have too many pets and not enough food, act angry.
            self.behavior \= self.act\_angry
        elif self.pet\_count < self.pet\_target and self.feed\_count \> self.feed\_target:
            \# If we have not enough pets and too much food, go to the bathroom.
            self.behavior \= self.go\_to\_bathroom
        elif self.pet\_count \== 0 and self.feed\_count \> 0:
            \# If we have no pets and some food, act playful.
            self.behavior \= self.act\_playful
        elif self.feed\_count \== 0:
            \# If we have no food, act hungry.
            self.behavior \= self.act\_hungry

    @property
    def eyes(self):
        """Gets and sets the eyes."""
        return self.\_eyes

    @eyes.setter
    def eyes(self, value):
        if value != self.\_eyes:
            self.\_eyes \= value
            self.ev3.screen.load\_image(value)

    def update\_eyes(self):
        if self.eyes\_timer\_1.time() \> self.eyes\_timer\_1\_end:
            self.eyes\_timer\_1.reset()
            if self.eyes \== self.SLEEPING\_EYES:
                self.eyes\_timer\_1\_end \= urandom.randint(1, 5) \* 1000
                self.eyes \= self.TIRED\_RIGHT\_EYES
            else:
                self.eyes\_timer\_1\_end \= 250
                self.eyes \= self.SLEEPING\_EYES

        if self.eyes\_timer\_2.time() \> self.eyes\_timer\_2\_end:
            self.eyes\_timer\_2.reset()
            if self.eyes != self.SLEEPING\_EYES:
                self.eyes\_timer\_2\_end \= urandom.randint(1, 10) \* 1000
                if self.eyes != self.TIRED\_LEFT\_EYES:
                    self.eyes \= self.TIRED\_LEFT\_EYES
                else:
                    self.eyes \= self.TIRED\_RIGHT\_EYES

    def update\_pet\_count(self):
        """Updates the :attr:\`pet\_count\` attribute if the puppy is currently
        being petted (touch sensor pressed).

        Returns:
            bool:
                \`\`True\`\` if the puppy was petted since the last time this method
                was called, otherwise \`\`False\`\`.
        """
        changed \= False

        petted \= self.touch\_sensor.pressed()
        if petted and petted != self.prev\_petted:
            self.pet\_count += 1
            print('pet\_count:', self.pet\_count, 'pet\_target:', self.pet\_target)
            self.count\_changed\_timer.reset()
            if not self.behavior \== self.act\_hungry:
                self.eyes \= self.SQUINTY\_EYES
                self.ev3.speaker.play\_file(SoundFile.DOG\_SNIFF)
            changed \= True

        self.prev\_petted \= petted
        return changed

    def update\_feed\_count(self):
        """Updates the :attr:\`feed\_count\` attribute if the puppy is currently
        being fed (color sensor detects a color).

        Returns:
            bool:
                \`\`True\`\` if the puppy was fed since the last time this method
                was called, otherwise \`\`False\`\`.
        """
        color \= self.color\_sensor.color()
        changed \= False

        if color is not None and color != Color.BLACK and color != self.prev\_color:
            self.feed\_count += 1
            print('feed\_count:', self.feed\_count, 'feed\_target:', self.feed\_target)
            changed \= True
            self.count\_changed\_timer.reset()
            self.prev\_color \= color
            self.eyes \= self.SQUINTY\_EYES
            self.ev3.speaker.play\_file(SoundFile.CRUNCHING)

        return changed

    def monitor\_counts(self):
        """Monitors pet and feed counts and decreases them over time."""
        if self.pet\_count\_timer.time() \> 15000:
            self.pet\_count\_timer.reset()
            self.pet\_count \= max(0, self.pet\_count \- 1)
            print('pet\_count:', self.pet\_count, 'pet\_target:', self.pet\_target)
        if self.feed\_count\_timer.time() \> 15000:
            self.feed\_count\_timer.reset()
            self.feed\_count \= max(0, self.feed\_count \- 1)
            print('feed\_count:', self.feed\_count, 'feed\_target:', self.feed\_target)
        if self.count\_changed\_timer.time() \> 30000:
            \# If nothing has happened for 30 seconds, go to sleep
            self.count\_changed\_timer.reset()
            self.behavior \= self.go\_to\_sleep

    def run(self):
        """This is the main program run loop."""
        self.sit\_down()
        self.adjust\_head()
        self.eyes \= self.SLEEPING\_EYES
        self.reset()
        while True:
            self.monitor\_counts()
            self.behavior()
            wait(100)

\# This covers up the tear to make a new image.
Puppy.SQUINTY\_EYES.draw\_box(120, 60, 140, 85, fill\=True, color\=Color.WHITE)

if \_\_name\_\_ \== '\_\_main\_\_':
    puppy \= Puppy()
    puppy.run()