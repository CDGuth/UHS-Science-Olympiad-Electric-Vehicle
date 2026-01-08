# Signals and Units[¶](#signals-and-units "Permalink to this headline")

Many commands allow you to specify arguments in terms of well-known physical quantities. This page gives an overview of each quantity and its unit.

## Time[¶](#time "Permalink to this headline")

### time: ms[¶](#time-ms "Permalink to this headline")

All time and duration values are measured in milliseconds (ms).

For example, the duration of motion with `run_time`, and the duration of [`wait`](tools.html#pybricks.tools.wait "pybricks.tools.wait") are specified in milliseconds.

## Angles and angular motion[¶](#angles-and-angular-motion "Permalink to this headline")

### angle: deg[¶](#angle-deg "Permalink to this headline")

All angles are measured in degrees (deg). One full rotation corresponds to 360 degrees.

For example, the angle values of a `Motor` or the [`GyroSensor`](ev3devices.html#pybricks.ev3devices.GyroSensor.angle "pybricks.ev3devices.GyroSensor.angle") are expressed in degrees.

### rotational speed: deg/s[¶](#rotational-speed-deg-s "Permalink to this headline")

Rotational speed, or _angular velocity_ describes how fast something rotates, expressed as the number of degrees per second (deg/s).

For example, the rotational speed values of a `Motor` or the [`GyroSensor`](ev3devices.html#pybricks.ev3devices.GyroSensor.speed "pybricks.ev3devices.GyroSensor.speed") are expressed in degrees per second.

While we recommend working with degrees per second in your programs, you can use the following table to convert between commonly used units.

  

 

deg/s

rpm

1 deg/s =

1

1/6=0.167

1 rpm =

6

1

### rotational acceleration: deg/s/s[¶](#rotational-acceleration-deg-s-s "Permalink to this headline")

Rotational acceleration, or _angular acceleration_ describes how fast the rotational speed changes. This is expressed as the change of the number of degrees per second, during one second (deg/s/s). This is also commonly written as \\(deg/s^2\\).

For example, you can adjust the rotational acceleration setting of a `Motor` to change how smoothly or how quickly it reaches the constant speed set point.

## Distance and linear motion[¶](#distance-and-linear-motion "Permalink to this headline")

### distance: mm[¶](#distance-mm "Permalink to this headline")

Distances are expressed in millimeters (mm) whenever possible.

For example, the distance value of the [`UltrasonicSensor`](ev3devices.html#pybricks.ev3devices.UltrasonicSensor.distance "pybricks.ev3devices.UltrasonicSensor.distance") is measured in millimeters.

While we recommend working with millimeters in your programs, you can use the following table to convert between commonly used units.

   

 

mm

cm

inch

1 mm =

1

0.1

0.0394

1 cm =

10

1

0.394

1 inch =

25.4

2.54

1

### dimension: mm[¶](#dimension-mm "Permalink to this headline")

Dimensions are expressed in millimeters (mm), just like distances.

For example, the diameter of a wheel is measured in millimeters.

### speed: mm/s[¶](#speed-mm-s "Permalink to this headline")

Linear speeds are expressed as millimeters per second (mm/s).

For example, the speed of a robotic vehicle is expressed in mm/s.

### linear acceleration: mm/s/s[¶](#linear-acceleration-mm-s-s "Permalink to this headline")

Linear acceleration describes how fast the speed changes. This is expressed as the change of the millimeters per second, during one second (deg/s/s). This is also commonly written as \\(mm/s^2\\).

For example, you can adjust the acceleration setting of a [`DriveBase`](robotics.html#pybricks.robotics.DriveBase "pybricks.robotics.DriveBase") to change how smoothly or how quickly it reaches the constant speed set point.

## Approximate and relative units[¶](#approximate-and-relative-units "Permalink to this headline")

### percentage: %[¶](#percentage "Permalink to this headline")

Some signals do not have specific units. They range from a minimum (0%) to a maximum (100%). Specifics type of percentages are [relative distances](#relativedistance) or [brightness](#brightness).

Another example is the sound volume, which ranges from 0% (silent) to 100% (loudest).

### relative distance: %[¶](#relative-distance "Permalink to this headline")

Some distance measurements do not provide an accurate value with a specific unit, but they range from very close (0%) to very far (100%). These are referred to as relative distances.

For example, the distance value of the [`InfraredSensor`](ev3devices.html#pybricks.ev3devices.InfraredSensor.distance "pybricks.ev3devices.InfraredSensor.distance") is a relative distance.

### brightness: %[¶](#brightness "Permalink to this headline")

The perceived brightness of a light is expressed as a percentage. It is 0% when the light is off and 100% when the light is fully on. When you choose 50%, this means that the light is perceived as approximately half as bright to the human eye.

## Force[¶](#force "Permalink to this headline")

### force: N[¶](#force-n "Permalink to this headline")

Force values are expressed in newtons (N).

While we recommend working with newtons in your programs, you can use the following table to convert to and from other units.

   

 

mN

N

lbf

1 mN =

1

0.001

\\(2.248 \\cdot 10^{-4}\\)

1 N =

1000

1

0.2248

1 lbf =

4448

4.448

1

## Electricity[¶](#electricity "Permalink to this headline")

### voltage: mV[¶](#voltage-mv "Permalink to this headline")

Voltages are expressed in millivolt (mV).

For example, you can check the voltage of the battery.

### current: mA[¶](#current-ma "Permalink to this headline")

Electrical currents are expressed in milliampere (mA).

For example, you can check the current supplied by the battery.

### energy: J[¶](#energy-j "Permalink to this headline")

Stored energy or energy consumption can be expressed in Joules (J).

### power: mW[¶](#power-mw "Permalink to this headline")

Power is the rate at which energy is stored or consumed. It is expressed in milliwatt (mW).

## Ambient environment[¶](#ambient-environment "Permalink to this headline")

### frequency: Hz[¶](#frequency-hz "Permalink to this headline")

Sound frequencies are expressed in Hertz (Hz).

For example, you can choose the frequency of a beep to change the pitch.

### temperature: °C[¶](#temperature-c "Permalink to this headline")

Temperature is measured in degrees Celcius (°C). To convert to degrees Fahrenheit (°F) or Kelvin (K), you can use the following conversion formulas:

> \\(°\\!F = °\\!C \\cdot \\frac{9}{5} + 32\\).
> 
> \\(K = °\\!C + 273.15\\).