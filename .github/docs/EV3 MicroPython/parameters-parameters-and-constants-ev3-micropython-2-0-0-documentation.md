# [`parameters`](#module-pybricks.parameters "pybricks.parameters") – Parameters and Constants[¶](#module-pybricks.parameters "Permalink to this headline")

Constant parameters/arguments for the Pybricks API.

_class_ `Port`[¶](#pybricks.parameters.Port "Permalink to this definition")

Port on the programmable brick or hub.

> Motor ports:
> 
> > `A`[¶](#pybricks.parameters.Port.A "Permalink to this definition")
> > 
> > `B`[¶](#pybricks.parameters.Port.B "Permalink to this definition")
> > 
> > `C`[¶](#pybricks.parameters.Port.C "Permalink to this definition")
> > 
> > `D`[¶](#pybricks.parameters.Port.D "Permalink to this definition")
> 
> Sensor ports:
> 
> > `S1`[¶](#pybricks.parameters.Port.S1 "Permalink to this definition")
> > 
> > `S2`[¶](#pybricks.parameters.Port.S2 "Permalink to this definition")
> > 
> > `S3`[¶](#pybricks.parameters.Port.S3 "Permalink to this definition")
> > 
> > `S4`[¶](#pybricks.parameters.Port.S4 "Permalink to this definition")

_class_ `Direction`[¶](#pybricks.parameters.Direction "Permalink to this definition")

Rotational direction for positive speed or angle values.

`CLOCKWISE`[¶](#pybricks.parameters.Direction.CLOCKWISE "Permalink to this definition")

A positive speed value should make the motor move clockwise.

`COUNTERCLOCKWISE`[¶](#pybricks.parameters.Direction.COUNTERCLOCKWISE "Permalink to this definition")

A positive speed value should make the motor move counterclockwise.

  

`positive_direction =`

Positive speed:

Negative speed:

`Direction.CLOCKWISE`

clockwise

counterclockwise

`Direction.COUNTERCLOCKWISE`

counterclockwise

clockwise

By default, the positive direction is set as clockwise. Refer to [this diagram](ev3devices.html#fig-ev3motors) to see which direction this is for EV3 motors.

_class_ `Stop`[¶](#pybricks.parameters.Stop "Permalink to this definition")

Action after the motor stops: coast, brake, or hold.

`COAST`[¶](#pybricks.parameters.Stop.COAST "Permalink to this definition")

Let the motor move freely.

`BRAKE`[¶](#pybricks.parameters.Stop.BRAKE "Permalink to this definition")

Passively resist small external forces.

`HOLD`[¶](#pybricks.parameters.Stop.HOLD "Permalink to this definition")

Keep controlling the motor to hold it at the commanded angle. This is only available on motors with encoders.

The following table show how each stop type adds an extra level of resistance to motion. In these examples, `m` is a [`Motor`](ev3devices.html#pybricks.ev3devices.Motor "pybricks.ev3devices.Motor") and and `d` is a [`DriveBase`](robotics.html#pybricks.robotics.DriveBase "pybricks.robotics.DriveBase"). The examples also show how running at zero speed compares to these stop types.

     

Type

Friction

Back

EMF

Speed

kept at 0

Angle kept

at target

Examples

Coast

 

 

 

`m.stop()`

`m.run_target(500, 90, Stop.COAST)`

Brake

 

 

`m.brake()`

`m.run_target(500, 90, Stop.BRAKE)`

 

 

`m.run(0)`

`d.drive(0, 0)`

Hold

`m.hold()`

`m.run_target(500, 90, Stop.HOLD)`

`d.straight(0)`

`d.straight(100)`

_class_ `Color`[¶](#pybricks.parameters.Color "Permalink to this definition")

Light or surface color.

`BLACK`[¶](#pybricks.parameters.Color.BLACK "Permalink to this definition")

`BLUE`[¶](#pybricks.parameters.Color.BLUE "Permalink to this definition")

`GREEN`[¶](#pybricks.parameters.Color.GREEN "Permalink to this definition")

`YELLOW`[¶](#pybricks.parameters.Color.YELLOW "Permalink to this definition")

`RED`[¶](#pybricks.parameters.Color.RED "Permalink to this definition")

`WHITE`[¶](#pybricks.parameters.Color.WHITE "Permalink to this definition")

`BROWN`[¶](#pybricks.parameters.Color.BROWN "Permalink to this definition")

`ORANGE`[¶](#pybricks.parameters.Color.ORANGE "Permalink to this definition")

`PURPLE`[¶](#pybricks.parameters.Color.PURPLE "Permalink to this definition")

_class_ `Button`[¶](#pybricks.parameters.Button "Permalink to this definition")

Buttons on a brick or remote:

`LEFT_DOWN`[¶](#pybricks.parameters.Button.LEFT_DOWN "Permalink to this definition")

`DOWN`[¶](#pybricks.parameters.Button.DOWN "Permalink to this definition")

`RIGHT_DOWN`[¶](#pybricks.parameters.Button.RIGHT_DOWN "Permalink to this definition")

`LEFT`[¶](#pybricks.parameters.Button.LEFT "Permalink to this definition")

`CENTER`[¶](#pybricks.parameters.Button.CENTER "Permalink to this definition")

`RIGHT`[¶](#pybricks.parameters.Button.RIGHT "Permalink to this definition")

`LEFT_UP`[¶](#pybricks.parameters.Button.LEFT_UP "Permalink to this definition")

`UP`[¶](#pybricks.parameters.Button.UP "Permalink to this definition")

`BEACON`[¶](#pybricks.parameters.Button.BEACON "Permalink to this definition")

`RIGHT_UP`[¶](#pybricks.parameters.Button.RIGHT_UP "Permalink to this definition")

  

LEFT\_UP

UP/BEACON

RIGHT\_UP

LEFT

CENTER

RIGHT

LEFT\_DOWN

DOWN

RIGHT\_DOWN