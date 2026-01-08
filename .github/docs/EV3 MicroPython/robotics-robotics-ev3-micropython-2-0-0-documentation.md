# [`robotics`](#module-pybricks.robotics "pybricks.robotics") – Robotics[¶](#module-pybricks.robotics "Permalink to this headline")

Robotics module for the Pybricks API.

_class_ `DriveBase`(_left\_motor_, _right\_motor_, _wheel\_diameter_, _axle\_track_)[¶](#pybricks.robotics.DriveBase "Permalink to this definition")

A robotic vehicle with two powered wheels and an optional support wheel or caster.

By specifying the dimensions of your robot, this class makes it easy to drive a given distance in millimeters or turn by a given number of degrees.

**Positive** distances and drive speeds mean driving **forward**. **Negative** means **backward**.

**Positive** angles and turn rates mean turning **right**. **Negative** means **left**. So when viewed from the top, positive means clockwise and negative means counterclockwise.

 

Parameters:

*   **left\_motor** ([_Motor_](ev3devices.html#pybricks.ev3devices.Motor "pybricks.ev3devices.Motor")) – The motor that drives the left wheel.
*   **right\_motor** ([_Motor_](ev3devices.html#pybricks.ev3devices.Motor "pybricks.ev3devices.Motor")) – The motor that drives the right wheel.
*   **wheel\_diameter** ([dimension: mm](signaltypes.html#dimension)) – Diameter of the wheels.
*   **axle\_track** ([dimension: mm](signaltypes.html#dimension)) – Distance between the points where both wheels touch the ground.

Driving for a given distance or by an angle

Use the following commands to drive a given distance, or turn by a given angle.

This is measured using the internal rotation sensors. Because wheels may slip while moving, the traveled distance and angle are only estimates.

`straight`(_distance_)[¶](#pybricks.robotics.DriveBase.straight "Permalink to this definition")

Drives straight for a given distance and then stops.

 

Parameters:

**distance** ([distance: mm](signaltypes.html#distance)) – Distance to travel.

`turn`(_angle_)[¶](#pybricks.robotics.DriveBase.turn "Permalink to this definition")

Turns in place by a given angle and then stops.

 

Parameters:

**angle** ([angle: deg](signaltypes.html#angle)) – Angle of the turn.

`settings`(_straight\_speed_, _straight\_acceleration_, _turn\_rate_, _turn\_acceleration_)[¶](#pybricks.robotics.DriveBase.settings "Permalink to this definition")

Configures the speed and acceleration used by [`straight()`](#pybricks.robotics.DriveBase.straight "pybricks.robotics.DriveBase.straight") and [`turn()`](#pybricks.robotics.DriveBase.turn "pybricks.robotics.DriveBase.turn").

If you give no arguments, this returns the current values as a tuple.

You can only change the settings while the robot is stopped. This is either before you begin driving or after you call [`stop()`](#pybricks.robotics.DriveBase.stop "pybricks.robotics.DriveBase.stop").

 

Parameters:

*   **straight\_speed** ([speed: mm/s](signaltypes.html#linspeed)) – Speed of the robot during [`straight()`](#pybricks.robotics.DriveBase.straight "pybricks.robotics.DriveBase.straight").
*   **straight\_acceleration** ([linear acceleration: mm/s/s](signaltypes.html#linacceleration)) – Acceleration and deceleration of the robot at the start and end of [`straight()`](#pybricks.robotics.DriveBase.straight "pybricks.robotics.DriveBase.straight").
*   **turn\_rate** ([rotational speed: deg/s](signaltypes.html#speed)) – Turn rate of the robot during [`turn()`](#pybricks.robotics.DriveBase.turn "pybricks.robotics.DriveBase.turn").
*   **turn\_acceleration** ([rotational acceleration: deg/s/s](signaltypes.html#acceleration)) – Angular acceleration and deceleration of the robot at the start and end of [`turn()`](#pybricks.robotics.DriveBase.turn "pybricks.robotics.DriveBase.turn").

Drive forever

Use [`drive()`](#pybricks.robotics.DriveBase.drive "pybricks.robotics.DriveBase.drive") to begin driving at a desired speed and steering.

It keeps going until you use [`stop()`](#pybricks.robotics.DriveBase.stop "pybricks.robotics.DriveBase.stop") or change course by using [`drive()`](#pybricks.robotics.DriveBase.drive "pybricks.robotics.DriveBase.drive") again. For example, you can drive until a sensor is triggered and then stop or turn around.

`drive`(_drive\_speed_, _turn\_rate_)[¶](#pybricks.robotics.DriveBase.drive "Permalink to this definition")

Starts driving at the specified speed and turn rate. Both values are measured at the center point between the wheels of the robot.

 

Parameters:

*   **drive\_speed** ([speed: mm/s](signaltypes.html#linspeed)) – Speed of the robot.
*   **turn\_rate** ([rotational speed: deg/s](signaltypes.html#speed)) – Turn rate of the robot.

`stop`()[¶](#pybricks.robotics.DriveBase.stop "Permalink to this definition")

Stops the robot by letting the motors spin freely.

Measuring

`distance`()[¶](#pybricks.robotics.DriveBase.distance "Permalink to this definition")

Gets the estimated driven distance.

 

Returns:

Driven distance since last reset.

Return type:

[distance: mm](signaltypes.html#distance)

`angle`()[¶](#pybricks.robotics.DriveBase.angle "Permalink to this definition")

Gets the estimated rotation angle of the drive base.

 

Returns:

Accumulated angle since last reset.

Return type:

[angle: deg](signaltypes.html#angle)

`state`()[¶](#pybricks.robotics.DriveBase.state "Permalink to this definition")

Gets the state of the robot.

This returns the current [`distance()`](#pybricks.robotics.DriveBase.distance "pybricks.robotics.DriveBase.distance"), the drive speed, the [`angle()`](#pybricks.robotics.DriveBase.angle "pybricks.robotics.DriveBase.angle"), and the turn rate.

 

Returns:

Distance, drive speed, angle, turn rate

Return type:

([distance: mm](signaltypes.html#distance), [speed: mm/s](signaltypes.html#linspeed), [angle: deg](signaltypes.html#angle), [rotational speed: deg/s](signaltypes.html#speed))

`reset`()[¶](#pybricks.robotics.DriveBase.reset "Permalink to this definition")

Resets the estimated driven distance and angle to 0.

Measuring and validating the robot dimensions

As a first estimate, you can measure the `wheel_diameter` and the `axle_track` with a ruler. Because it is hard to see where the wheels effectively touch the ground, you can estimate the `axle_track` as the distance between the midpoint of the wheels.

In practice, most wheels compress slightly under the weight of your robot. To verify, make your robot drive 1000 mm using `my_robot.straight(1000)` and measure how far it really traveled. Compensate as follows:

> *   If your robot drives **not far enough**, **decrease** the `wheel_diameter` value slightly.
> *   If your robot drives **too far**, **increase** the `wheel_diameter` value slightly.

Motor shafts and axles bend slightly under the load of the robot, causing the ground contact point of the wheels to be closer to the midpoint of your robot. To verify, make your robot turn 360 degrees using `my_robot.turn(360)` and check that it is back in the same place:

> *   If your robot turns **not far enough**, **increase** the `axle_track` value slightly.
> *   If your robot turns **too far**, **decrease** the `axle_track` value slightly.

When making these adjustments, always adjust the `wheel_diameter` first, as done above. Be sure to test both turning and driving straight after you are done.

Using the DriveBase motors individually

Suppose you make a [`DriveBase`](#pybricks.robotics.DriveBase "pybricks.robotics.DriveBase") object using two `Motor` objects called `left_motor` and `right_motor`. You **cannot** use these motors individually while the DriveBase is **active**.

The DriveBase is active if it is driving, but also when it is actively holding the wheels in place after a [`straight()`](#pybricks.robotics.DriveBase.straight "pybricks.robotics.DriveBase.straight") or [`turn()`](#pybricks.robotics.DriveBase.turn "pybricks.robotics.DriveBase.turn") command. To deactivate the [`DriveBase`](#pybricks.robotics.DriveBase "pybricks.robotics.DriveBase"), call [`stop()`](#pybricks.robotics.DriveBase.stop "pybricks.robotics.DriveBase.stop").

Advanced Settings

The [`settings()`](#pybricks.robotics.DriveBase.settings "pybricks.robotics.DriveBase.settings") method is used to adjust commonly used settings like the default speed and acceleration for straight maneuvers and turns. Use the following attributes to adjust more advanced control setttings.

You can only change the settings while the robot is stopped. This is either before you begin driving or after you call [`stop()`](#pybricks.robotics.DriveBase.stop "pybricks.robotics.DriveBase.stop").

`distance_control`[¶](#pybricks.robotics.DriveBase.distance_control "Permalink to this definition")

The traveled distance and drive speed are controlled by a PID controller. You can use this attribute to change its settings. See [The Control Class](motors.html#control) for an overview of available methods.

`heading_control`[¶](#pybricks.robotics.DriveBase.heading_control "Permalink to this definition")

The robot turn angle and turn rate are controlled by a PID controller. You can use this attribute to change its settings. See [The Control Class](motors.html#control) for an overview of available methods.