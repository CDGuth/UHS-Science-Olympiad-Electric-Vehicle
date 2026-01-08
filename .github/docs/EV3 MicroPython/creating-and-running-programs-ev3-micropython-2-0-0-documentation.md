# Creating and running programs[¶](#creating-and-running-programs "Permalink to this headline")

Now that you’ve set up your computer and EV3 Brick, you’re ready to start writing programs.

To make it easier to create and manage your programs, let’s first have a quick look at how MicroPython projects and programs for your EV3 robots are organized.

Programs are organized into _project folders_, as shown in [Figure 8](#fig-projectstructure). A project folder is a directory on your computer that contains the main program (**main.py**) and other optional scripts or files. This project folder and all of its contents will be copied to the EV3 Brick, where the main program will be run.

This page shows you how to create such a project and how to transfer it to the EV3 Brick.

![projectstructure](_images/projectstructure_label.png)

Figure 8 A project contains a program called **main.py** and optional resources like sounds or MicroPython modules.

## Creating a new project[¶](#creating-a-new-project "Permalink to this headline")

To create a new project, open the EV3 MicroPython tab and click _create a new project_, as shown in [Figure 9](#fig-newproject). Enter a project name in the text field that appears and press _Enter_. When prompted, choose a location for this program and confirm by clicking _choose folder_.

![newproject](_images/newproject_label.png)

Figure 9 Creating a new project. This example is called _getting\_started_, but you can choose any name.

When you create a new project, it already includes a file called _main.py_. To see its contents and to modify it, open it from the file browser as shown in [Figure 10](#fig-projectoverview). This is where you’ll write your programs.

If you are new to MicroPython programming, we recommend that you keep the existing code in place and add your code to it.

![projectoverview](_images/projectoverview_label.png)

Figure 10 Opening the default _main.py_ program.

## Opening an existing project[¶](#opening-an-existing-project "Permalink to this headline")

To open a project you created previously, click _File_ and click _Open Folder_, as shown in [Figure 11](#fig-existingproject). Next, navigate to your previously created project folder and click _OK_. You can also open your recently used projects using the _Open Recent_ menu option.

![existingproject](_images/existingproject_label.png)

Figure 11 Opening a previously created project.

## Connecting to the EV3 Brick with Visual Studio Code[¶](#connecting-to-the-ev3-brick-with-visual-studio-code "Permalink to this headline")

To be able to transfer your code to the EV3 Brick, you’ll first need to connect the EV3 Brick to your computer with the mini-USB cable and configure the connection with Visual Studio Code. To do so:

*   Turn the EV3 Brick on
*   Connect the EV3 Brick to your computer with the mini-USB cable
*   Configure the USB connection as shown in [Figure 12](#fig-connecting).

![connecting](_images/connecting_label.png)

Figure 12 Configuring the USB connection between the computer and the EV3 Brick

## Downloading and running a program[¶](#downloading-and-running-a-program "Permalink to this headline")

You can press the F5 key to run the program. Alternatively, you can start it manually by going to the _debug_ tab and clicking the green start arrow, as shown in [Figure 13](#fig-running).

When the program starts, a pop-up toolbar allows you to stop the program if necessary. You can also stop the program at any time using the back button on the EV3 Brick.

If your program produces any output with the `print` command, this is shown in the output window.

![running](_images/running_label.png)

Figure 13 Running a program

## Expanding the example program[¶](#expanding-the-example-program "Permalink to this headline")

Now that you’ve run the basic code template, you can expand the program to make a motor move. First, attach a Large Motor to Port B on the EV3 Brick, as shown in [Figure 14](#fig-firstprogram).

![firstprogram](_images/firstprogram_label.png)

Figure 14 The EV3 Brick with a Large Motor attached to port B.

Next, edit _main.py_ to make it look like this:

#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

\# Create your objects here

\# Initialize the EV3 Brick.
ev3 \= EV3Brick()

\# Initialize a motor at port B.
test\_motor \= Motor(Port.B)

\# Write your program here

\# Play a sound.
ev3.speaker.beep()

\# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
test\_motor.run\_target(500, 90)

\# Play another beep sound.
ev3.speaker.beep(frequency\=1000, duration\=500)

This program makes your robot beep, rotate the motor, and beep again with a higher pitched tone. Run the program to make sure that it works as expected.

## Managing files on the EV3 Brick[¶](#managing-files-on-the-ev3-brick "Permalink to this headline")

After you’ve downloaded a project to the EV3 Brick, you can run, delete, or back up programs stored on it using the device browser as shown in [Figure 15](#fig-files).

![files](_images/files_label.png)

Figure 15 Using the EV3 device browser to manage files on your EV3 Brick