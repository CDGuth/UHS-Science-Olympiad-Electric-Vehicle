# [`ev3devices`](#module-pybricks.ev3devices "pybricks.ev3devices") – EV3 Devices[¶](#module-pybricks.ev3devices "Permalink to this headline")

LEGO® MINDSTORMS® EV3 motors and sensors.

## Motors[¶](#motors "Permalink to this headline")

![_images/ev3motors_label.png](_images/ev3motors_label.png)

Figure 17 EV3-compatible motors. The arrows indicate the default positive direction.

_class_ `Motor`(_port_, _positive\_direction=Direction.CLOCKWISE_, _gears=None_)[¶](#pybricks.ev3devices.Motor "Permalink to this definition")

Generic class to control motors with built-in rotation sensors.

 

Parameters:

*   **port** ([_Port_](parameters.html#pybricks.parameters.Port "pybricks.parameters.Port")) – Port to which the motor is connected.
*   **positive\_direction** ([_Direction_](parameters.html#pybricks.parameters.Direction "pybricks.parameters.Direction")) – Which direction the motor should turn when you give a positive speed value or angle.
*   **gears** (_list_) –
    
    List of gears linked to the motor.
    
    For example: `[12, 36]` represents a gear train with a 12-tooth and a 36-tooth gear. Use a list of lists for multiple gear trains, such as `[[12, 36], [20, 16, 40]]`.
    
    When you specify a gear train, all motor commands and settings are automatically adjusted to account for the resulting gear ratio. The motor direction remains unchanged by this.
    

Measuring

`speed`()[¶](#pybricks.ev3devices.Motor.speed "Permalink to this definition")

Gets the speed of the motor.

 

Returns:

Motor speed.

Return type:

[rotational speed: deg/s](signaltypes.html#speed)

`angle`()[¶](#pybricks.ev3devices.Motor.angle "Permalink to this definition")

Gets the rotation angle of the motor.

 

Returns:

Motor angle.

Return type:

[angle: deg](signaltypes.html#angle)

`reset_angle`(_angle_)[¶](#pybricks.ev3devices.Motor.reset_angle "Permalink to this definition")

Sets the accumulated rotation angle of the motor to a desired value.

 

Parameters:

**angle** ([angle: deg](signaltypes.html#angle)) – Value to which the angle should be reset.

Stopping

`stop`()[¶](#pybricks.ev3devices.Motor.stop "Permalink to this definition")

Stops the motor and lets it spin freely.

The motor gradually stops due to friction.

`brake`()[¶](#pybricks.ev3devices.Motor.brake "Permalink to this definition")

Passively brakes the motor.

The motor stops due to friction, plus the voltage that is generated while the motor is still moving.

`hold`()[¶](#pybricks.ev3devices.Motor.hold "Permalink to this definition")

Stops the motor and actively holds it at its current angle.

Action

`run`(_speed_)[¶](#pybricks.ev3devices.Motor.run "Permalink to this definition")

Runs the motor at a constant speed.

The motor accelerates to the given speed and keeps running at this speed until you give a new command.

 

Parameters:

**speed** ([rotational speed: deg/s](signaltypes.html#speed)) – Speed of the motor.

`run_time`(_speed_, _time_, _then=Stop.HOLD_, _wait=True_)[¶](#pybricks.ev3devices.Motor.run_time "Permalink to this definition")

Runs the motor at a constant speed for a given amount of time.

The motor accelerates to the given speed, keeps running at this speed, and then decelerates. The total maneuver lasts for exactly the given amount of `time`.

 

Parameters:

*   **speed** ([rotational speed: deg/s](signaltypes.html#speed)) – Speed of the motor.
*   **time** ([time: ms](signaltypes.html#id1)) – Duration of the maneuver.
*   **then** ([_Stop_](parameters.html#pybricks.parameters.Stop "pybricks.parameters.Stop")) – What to do after coming to a standstill.
*   **wait** (_bool_) – Wait for the maneuver to complete before continuing with the rest of the program.

`run_angle`(_speed_, _rotation\_angle_, _then=Stop.HOLD_, _wait=True_)[¶](#pybricks.ev3devices.Motor.run_angle "Permalink to this definition")

Runs the motor at a constant speed by a given angle.

 

Parameters:

*   **speed** ([rotational speed: deg/s](signaltypes.html#speed)) – Speed of the motor.
*   **rotation\_angle** ([angle: deg](signaltypes.html#angle)) – Angle by which the motor should rotate.
*   **then** ([_Stop_](parameters.html#pybricks.parameters.Stop "pybricks.parameters.Stop")) – What to do after coming to a standstill.
*   **wait** (_bool_) – Wait for the maneuver to complete before continuing with the rest of the program.

`run_target`(_speed_, _target\_angle_, _then=Stop.HOLD_, _wait=True_)[¶](#pybricks.ev3devices.Motor.run_target "Permalink to this definition")

Runs the motor at a constant speed towards a given target angle.

The direction of rotation is automatically selected based on the target angle. It does matter if `speed` is positive or negative.

 

Parameters:

*   **speed** ([rotational speed: deg/s](signaltypes.html#speed)) – Speed of the motor.
*   **target\_angle** ([angle: deg](signaltypes.html#angle)) – Angle that the motor should rotate to.
*   **then** ([_Stop_](parameters.html#pybricks.parameters.Stop "pybricks.parameters.Stop")) – What to do after coming to a standstill.
*   **wait** (_bool_) – Wait for the motor to reach the target before continuing with the rest of the program.

`run_until_stalled`(_speed_, _then=Stop.COAST_, _duty\_limit=None_)[¶](#pybricks.ev3devices.Motor.run_until_stalled "Permalink to this definition")

Runs the motor at a constant speed until it stalls.

 

Parameters:

*   **speed** ([rotational speed: deg/s](signaltypes.html#speed)) – Speed of the motor.
*   **then** ([_Stop_](parameters.html#pybricks.parameters.Stop "pybricks.parameters.Stop")) – What to do after coming to a standstill.
*   **duty\_limit** ([percentage: %](signaltypes.html#percentage)) – Torque limit during this command. This is useful to avoid applying the full motor torque to a geared or lever mechanism.

Returns:

Angle at which the motor becomes stalled.

Return type:

[angle: deg](signaltypes.html#angle)

`dc`(_duty_)[¶](#pybricks.ev3devices.Motor.dc "Permalink to this definition")

Rotates the motor at a given duty cycle (also known as “power”).

This method lets you use a motor just like a simple DC motor.

 

Parameters:

**duty** ([percentage: %](signaltypes.html#percentage)) – The duty cycle (-100.0 to 100).

Advanced motion control

`track_target`(_target\_angle_)[¶](#pybricks.ev3devices.Motor.track_target "Permalink to this definition")

Tracks a target angle. This is similar to [`run_target()`](#pybricks.ev3devices.Motor.run_target "pybricks.ev3devices.Motor.run_target"), but the usual smooth acceleration is skipped: it will move to the target angle as fast as possible. This method is useful if you want to continuously change the target angle.

 

Parameters:

**target\_angle** ([angle: deg](signaltypes.html#angle)) – Target angle that the motor should rotate to.

`control`[¶](#pybricks.ev3devices.Motor.control "Permalink to this definition")

The motors use PID control to accurately track the speed and angle targets that you specify. You can change its behavior through the `control` attribute of the motor. See [The Control Class](motors.html#control) for an overview of available methods.

## Touch Sensor[¶](#touch-sensor "Permalink to this headline")

![_images/sensor_ev3_touch.png](_images/sensor_ev3_touch.png)

_class_ `TouchSensor`(_port_)[¶](#pybricks.ev3devices.TouchSensor "Permalink to this definition")

LEGO® MINDSTORMS® EV3 Touch Sensor.

 

Parameters:

**port** ([_Port_](parameters.html#pybricks.parameters.Port "pybricks.parameters.Port")) – Port to which the sensor is connected.

`pressed`()[¶](#pybricks.ev3devices.TouchSensor.pressed "Permalink to this definition")

Checks if the sensor is pressed.

 

Returns:

`True` if the sensor is pressed, `False` if it is not pressed.

Return type:

bool

## Color Sensor[¶](#color-sensor "Permalink to this headline")

![_images/sensor_ev3_color.png](_images/sensor_ev3_color.png)

_class_ `ColorSensor`(_port_)[¶](#pybricks.ev3devices.ColorSensor "Permalink to this definition")

LEGO® MINDSTORMS® EV3 Color Sensor.

 

Parameters:

**port** ([_Port_](parameters.html#pybricks.parameters.Port "pybricks.parameters.Port")) – Port to which the sensor is connected.

`color`()[¶](#pybricks.ev3devices.ColorSensor.color "Permalink to this definition")

Measures the color of a surface.

 

Returns:

`Color.BLACK`, `Color.BLUE`, `Color.GREEN`, `Color.YELLOW`, `Color.RED`, `Color.WHITE`, `Color.BROWN` or `None`.

Return type:

[`Color`](parameters.html#pybricks.parameters.Color "pybricks.parameters.Color"), or `None` if no color is detected.

`ambient`()[¶](#pybricks.ev3devices.ColorSensor.ambient "Permalink to this definition")

Measures the ambient light intensity.

 

Returns:

Ambient light intensity, ranging from 0 (dark) to 100 (bright).

Return type:

[percentage: %](signaltypes.html#percentage)

`reflection`()[¶](#pybricks.ev3devices.ColorSensor.reflection "Permalink to this definition")

Measures the reflection of a surface using a red light.

 

Returns:

Reflection, ranging from 0 (no reflection) to 100 (high reflection).

Return type:

[percentage: %](signaltypes.html#percentage)

`rgb`()[¶](#pybricks.ev3devices.ColorSensor.rgb "Permalink to this definition")

Measures the reflection of a surface using a red, green, and then a blue light.

 

Returns:

Tuple of reflections for red, green, and blue light, each ranging from 0.0 (no reflection) to 100.0 (high reflection).

Return type:

([percentage: %](signaltypes.html#percentage), [percentage: %](signaltypes.html#percentage), [percentage: %](signaltypes.html#percentage))

## Infrared Sensor and Beacon[¶](#infrared-sensor-and-beacon "Permalink to this headline")

![_images/sensor_ev3_ir.png](_images/sensor_ev3_ir.png)

_class_ `InfraredSensor`(_port_)[¶](#pybricks.ev3devices.InfraredSensor "Permalink to this definition")

LEGO® MINDSTORMS® EV3 Infrared Sensor and Beacon.

 

Parameters:

**port** ([_Port_](parameters.html#pybricks.parameters.Port "pybricks.parameters.Port")) – Port to which the sensor is connected.

`distance`()[¶](#pybricks.ev3devices.InfraredSensor.distance "Permalink to this definition")

Measures the relative distance between the sensor and an object using infrared light.

 

Returns:

Relative distance ranging from 0 (closest) to 100 (farthest).

Return type:

[relative distance: %](signaltypes.html#relativedistance)

`beacon`(_channel_)[¶](#pybricks.ev3devices.InfraredSensor.beacon "Permalink to this definition")

Measures the relative distance and angle between the remote and the infrared sensor.

 

Parameters:

**channel** (_int_) – Channel number of the remote.

Returns:

Tuple of relative distance (0 to 100) and approximate angle (-75 to 75 degrees) between remote and infrared sensor.

Return type:

([relative distance: %](signaltypes.html#relativedistance), [angle: deg](signaltypes.html#angle)) or (`None`, `None`) if no remote is detected.

`buttons`(_channel_)[¶](#pybricks.ev3devices.InfraredSensor.buttons "Permalink to this definition")

Checks which buttons on the infrared remote are pressed.

This method can detect up to two buttons at once. If you press more buttons, you may not get useful data.

 

Parameters:

**channel** (_int_) – Channel number of the remote.

Returns:

List of pressed buttons on the remote on selected channel.

Return type:

List of [`Button`](parameters.html#pybricks.parameters.Button "pybricks.parameters.Button")

`keypad`()[¶](#pybricks.ev3devices.InfraredSensor.keypad "Permalink to this definition")

Checks which buttons on the infrared remote are pressed.

This method can independently detect all 4 up/down buttons, but it cannot detect the beacon button.

This method only works with the remote in channel 1.

 

Returns:

List of pressed buttons on the remote on selected channel.

Return type:

List of [`Button`](parameters.html#pybricks.parameters.Button "pybricks.parameters.Button")

## Ultrasonic Sensor[¶](#ultrasonic-sensor "Permalink to this headline")

![_images/sensor_ev3_ultrasonic.png](_images/sensor_ev3_ultrasonic.png)

_class_ `UltrasonicSensor`(_port_)[¶](#pybricks.ev3devices.UltrasonicSensor "Permalink to this definition")

LEGO® MINDSTORMS® EV3 Ultrasonic Sensor.

 

Parameters:

**port** ([_Port_](parameters.html#pybricks.parameters.Port "pybricks.parameters.Port")) – Port to which the sensor is connected.

`distance`(_silent=False_)[¶](#pybricks.ev3devices.UltrasonicSensor.distance "Permalink to this definition")

Measures the distance between the sensor and an object using ultrasonic sound waves.

 

Parameters:

**silent** (_bool_) – Choose `True` to turn the sensor off after measuring the distance. This reduces interference with other ultrasonic sensors. If you do this too frequently, the sensor can freeze. If this happens, unplug it and plug it back in.

Returns:

Distance.

Return type:

[distance: mm](signaltypes.html#distance)

`presence`()[¶](#pybricks.ev3devices.UltrasonicSensor.presence "Permalink to this definition")

Checks for the presence of other ultrasonic sensors by detecting ultrasonic sounds.

If the other ultrasonic sensor is operating in silent mode, you can only detect the presence of that sensor while it is taking a measurement.

 

Returns:

`True` if ultrasonic sounds are detected, `False` if not.

Return type:

bool

## Gyroscopic Sensor[¶](#gyroscopic-sensor "Permalink to this headline")

![_images/sensor_ev3_gyro.png](_images/sensor_ev3_gyro.png)

_class_ `GyroSensor`(_port_, _positive\_direction=Direction.CLOCKWISE_)[¶](#pybricks.ev3devices.GyroSensor "Permalink to this definition")

LEGO® MINDSTORMS® EV3 Gyro Sensor.

 

Parameters:

*   **port** ([_Port_](parameters.html#pybricks.parameters.Port "pybricks.parameters.Port")) – Port to which the sensor is connected.
*   **positive\_direction** ([_Direction_](parameters.html#pybricks.parameters.Direction "pybricks.parameters.Direction")) – Positive rotation direction when looking at the red dot on top of the sensor.

`speed`()[¶](#pybricks.ev3devices.GyroSensor.speed "Permalink to this definition")

Gets the speed (angular velocity) of the sensor.

 

Returns:

Sensor angular velocity.

Return type:

[rotational speed: deg/s](signaltypes.html#speed)

`angle`()[¶](#pybricks.ev3devices.GyroSensor.angle "Permalink to this definition")

Gets the accumulated angle of the sensor.

 

Returns:

Rotation angle.

Return type:

[angle: deg](signaltypes.html#angle)

If you use the [`angle()`](#pybricks.ev3devices.GyroSensor.angle "pybricks.ev3devices.GyroSensor.angle") method, you cannot use the [`speed()`](#pybricks.ev3devices.GyroSensor.speed "pybricks.ev3devices.GyroSensor.speed") method in the same program. Doing so would reset the sensor angle to zero every time you read the speed.

`reset_angle`(_angle_)[¶](#pybricks.ev3devices.GyroSensor.reset_angle "Permalink to this definition")

Sets the rotation angle of the sensor to a desired value.

 

Parameters:

**angle** ([angle: deg](signaltypes.html#angle)) – Value to which the angle should be reset.