# More about Motors[¶](#more-about-motors "Permalink to this headline")

## The Control Class[¶](#the-control-class "Permalink to this headline")

The `Motor` class uses PID control to accurately track your commanded target angles. Similarly, the `DriveBase` class uses two of such controllers: one to control the heading and one to control the traveled distance.

You can change the control settings through the following attributes, which are instances of the `Control` class given below.:

> *   `Motor.control`
> *   `DriveBase.heading_control`
> *   `DriveBase.distance_control`

You can only change the settings while the controller is stopped. For example, you can set the settings at the beginning of your program. Alternatively, first call `stop()` to make your `Motor` or `DriveBase` stop, and then change the settings.

_class_ `Control`[¶](#pybricks._common.Control "Permalink to this definition")

Class to interact with PID controller and settings.

`scale`[¶](#pybricks._common.Control.scale "Permalink to this definition")

Scaling factor between the controlled integer variable and the physical output. For example, for a single motor this is the number of encoder pulses per degree of rotation.

Status

`done`()[¶](#pybricks._common.Control.done "Permalink to this definition")

Checks if an ongoing command or maneuver is done.

 

Returns:

`True` if the command is done, `False` if not.

Return type:

bool

`stalled`()[¶](#pybricks._common.Control.stalled "Permalink to this definition")

Checks if the controller is currently stalled.

A controller is stalled when it cannot reach the target speed or position, even with the maximum actuation signal.

 

Returns:

`True` if the controller is stalled, `False` if not.

Return type:

bool

Settings

`limits`(_speed_, _acceleration_, _actuation_)[¶](#pybricks._common.Control.limits "Permalink to this definition")

Configures the maximum speed, acceleration, and actuation.

If no arguments are given, this will return the current values.

 

Parameters:

*   **speed** ([rotational speed: deg/s](signaltypes.html#speed) or [speed: mm/s](signaltypes.html#linspeed)) – Maximum speed. All speed commands will be capped to this value.
*   **acceleration** ([rotational acceleration: deg/s/s](signaltypes.html#acceleration) or [linear acceleration: mm/s/s](signaltypes.html#linacceleration)) – Maximum acceleration.
*   **actuation** ([percentage: %](signaltypes.html#percentage)) – Maximum actuation as percentage of absolute maximum.

`pid`(_kp_, _ki_, _kd_, _integral\_range_, _integral\_rate_, _feed\_forward_)[¶](#pybricks._common.Control.pid "Permalink to this definition")

Gets or sets the PID values for position and speed control.

If no arguments are given, this will return the current values.

 

Parameters:

*   **kp** (_int_) – Proportional position (or integral speed) control constant.
*   **ki** (_int_) – Integral position control constant.
*   **kd** (_int_) – Derivative position (or proportional speed) control constant.
*   **integral\_range** ([angle: deg](signaltypes.html#angle) or [distance: mm](signaltypes.html#distance)) – Region around the target angle or distance, in which integral control errors are accumulated.
*   **integral\_rate** ([rotational speed: deg/s](signaltypes.html#speed) or [speed: mm/s](signaltypes.html#linspeed)) – Maximum rate at which the error integral is allowed to grow.
*   **feed\_forward** ([percentage: %](signaltypes.html#percentage)) – This adds a feed forward signal to the PID feedback signal, in the direction of the speed reference. This value is expressed as a percentage of the absolute maximum duty cycle.

`target_tolerances`(_speed_, _position_)[¶](#pybricks._common.Control.target_tolerances "Permalink to this definition")

Gets or sets the tolerances that say when a maneuver is done.

If no arguments are given, this will return the current values.

 

Parameters:

*   **speed** ([rotational speed: deg/s](signaltypes.html#speed) or [speed: mm/s](signaltypes.html#linspeed)) – Allowed deviation from zero speed before motion is considered complete.
*   **position** ([angle: deg](signaltypes.html#angle) or [distance: mm](signaltypes.html#distance)) – Allowed deviation from the target before motion is considered complete.

`stall_tolerances`(_speed_, _time_)[¶](#pybricks._common.Control.stall_tolerances "Permalink to this definition")

Gets or sets stalling tolerances.

If no arguments are given, this will return the current values.

 

Parameters:

*   **speed** ([rotational speed: deg/s](signaltypes.html#speed) or [speed: mm/s](signaltypes.html#linspeed)) – If the controller cannot reach this speed for some `time` even with maximum actuation, it is stalled.
*   **time** ([time: ms](signaltypes.html#id1)) – How long the controller has to be below this minimum `speed` before we say it is stalled.