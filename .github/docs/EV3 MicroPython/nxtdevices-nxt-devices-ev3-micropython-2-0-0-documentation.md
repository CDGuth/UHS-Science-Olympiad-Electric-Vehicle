# [`nxtdevices`](#module-pybricks.nxtdevices "pybricks.nxtdevices") – NXT Devices[¶](#module-pybricks.nxtdevices "Permalink to this headline")

Use LEGO® MINDSTORMS® NXT motors and sensors with the EV3 brick.

## NXT Motor[¶](#nxt-motor "Permalink to this headline")

This motor works just like a LEGO MINDSTORMS EV3 Large Motor. You can use it in your programs using the [`Motor`](ev3devices.html#module-pybricks.ev3devices "pybricks.ev3devices") class.

## NXT Touch Sensor[¶](#nxt-touch-sensor "Permalink to this headline")

![_images/sensor_nxt_touch.png](_images/sensor_nxt_touch.png)

_class_ `TouchSensor`(_port_)[¶](#pybricks.nxtdevices.TouchSensor "Permalink to this definition")

LEGO® MINDSTORMS® NXT Touch Sensor.

 

Parameters:

**port** ([_Port_](parameters.html#pybricks.parameters.Port "pybricks.parameters.Port")) – Port to which the sensor is connected.

`pressed`()[¶](#pybricks.nxtdevices.TouchSensor.pressed "Permalink to this definition")

Checks if the sensor is pressed.

 

Returns:

`True` if the sensor is pressed, `False` if it is not pressed.

Return type:

bool

## NXT Light Sensor[¶](#nxt-light-sensor "Permalink to this headline")

![_images/sensor_nxt_light.png](_images/sensor_nxt_light.png)

_class_ `LightSensor`(_port_)[¶](#pybricks.nxtdevices.LightSensor "Permalink to this definition")

LEGO® MINDSTORMS® NXT Color Sensor.

 

Parameters:

**port** ([_Port_](parameters.html#pybricks.parameters.Port "pybricks.parameters.Port")) – Port to which the sensor is connected.

`ambient`()[¶](#pybricks.nxtdevices.LightSensor.ambient "Permalink to this definition")

Measures the ambient light intensity.

 

Returns:

Ambient light intensity, ranging from 0 (dark) to 100 (bright).

Return type:

[percentage: %](signaltypes.html#percentage)

`reflection`()[¶](#pybricks.nxtdevices.LightSensor.reflection "Permalink to this definition")

Measures the reflection of a surface using a red light.

 

Returns:

Reflection, ranging from 0 (no reflection) to 100 (high reflection).

Return type:

[percentage: %](signaltypes.html#percentage)

## NXT Color Sensor[¶](#nxt-color-sensor "Permalink to this headline")

![_images/sensor_nxt_color.png](_images/sensor_nxt_color.png)

_class_ `ColorSensor`(_port_)[¶](#pybricks.nxtdevices.ColorSensor "Permalink to this definition")

LEGO® MINDSTORMS® NXT Color Sensor.

 

Parameters:

**port** ([_Port_](parameters.html#pybricks.parameters.Port "pybricks.parameters.Port")) – Port to which the sensor is connected.

`color`()[¶](#pybricks.nxtdevices.ColorSensor.color "Permalink to this definition")

Measures the color of a surface.

 

Returns:

`Color.BLACK`, `Color.BLUE`, `Color.GREEN`, `Color.YELLOW`, `Color.RED`, `Color.WHITE` or `None`.

Return type:

[`Color`](parameters.html#pybricks.parameters.Color "pybricks.parameters.Color"), or `None` if no color is detected.

`ambient`()[¶](#pybricks.nxtdevices.ColorSensor.ambient "Permalink to this definition")

Measures the ambient light intensity.

 

Returns:

Ambient light intensity, ranging from 0 (dark) to 100 (bright).

Return type:

[percentage: %](signaltypes.html#percentage)

`reflection`()[¶](#pybricks.nxtdevices.ColorSensor.reflection "Permalink to this definition")

Measures the reflection of a surface.

 

Returns:

Reflection, ranging from 0 (no reflection) to 100 (high reflection).

Return type:

[percentage: %](signaltypes.html#percentage)

`rgb`()[¶](#pybricks.nxtdevices.ColorSensor.rgb "Permalink to this definition")

Measures the reflection of a surface using a red, green, and then a blue light.

 

Returns:

Tuple of reflections for red, green, and blue light, each ranging from 0.0 (no reflection) to 100.0 (high reflection).

Return type:

([percentage: %](signaltypes.html#percentage), [percentage: %](signaltypes.html#percentage), [percentage: %](signaltypes.html#percentage))

Built-in light

This sensor has a built-in light. You can make it red, green, blue, or turn it off.

`light.``on`(_color_)[¶](#pybricks.nxtdevices.ColorSensor.light.on "Permalink to this definition")

Turns on the light at the specified color.

 

Parameters:

**color** ([_Color_](parameters.html#pybricks.parameters.Color "pybricks.parameters.Color")) – Color of the light. The light turns off if you choose `None` or a color that is not available.

`light.``off`()[¶](#pybricks.nxtdevices.ColorSensor.light.off "Permalink to this definition")

Turns off the light.

## NXT Ultrasonic Sensor[¶](#nxt-ultrasonic-sensor "Permalink to this headline")

![_images/sensor_nxt_ultrasonic.png](_images/sensor_nxt_ultrasonic.png)

_class_ `UltrasonicSensor`(_port_)[¶](#pybricks.nxtdevices.UltrasonicSensor "Permalink to this definition")

LEGO® MINDSTORMS® NXT Ultrasonic Sensor.

 

Parameters:

**port** ([_Port_](parameters.html#pybricks.parameters.Port "pybricks.parameters.Port")) – Port to which the sensor is connected.

`distance`()[¶](#pybricks.nxtdevices.UltrasonicSensor.distance "Permalink to this definition")

Measures the distance between the sensor and an object using ultrasonic sound waves.

 

Returns:

Distance.

Return type:

[distance: mm](signaltypes.html#distance)

## NXT Sound Sensor[¶](#nxt-sound-sensor "Permalink to this headline")

![_images/sensor_nxt_sound.png](_images/sensor_nxt_sound.png)

_class_ `SoundSensor`(_port_)[¶](#pybricks.nxtdevices.SoundSensor "Permalink to this definition")

LEGO® MINDSTORMS® NXT Sound Sensor.

 

Parameters:

**port** ([_Port_](parameters.html#pybricks.parameters.Port "pybricks.parameters.Port")) – Port to which the sensor is connected.

`intensity`(_audible\_only=True_)[¶](#pybricks.nxtdevices.SoundSensor.intensity "Permalink to this definition")

Measures the ambient sound intensity (loudness).

 

Parameters:

**audible\_only** (_bool_) – Detect only audible sounds. This tries to filter out frequencies that cannot be heard by the human ear.

Returns:

Sound intensity.

Return type:

[percentage: %](signaltypes.html#percentage)

## NXT Temperature Sensor[¶](#nxt-temperature-sensor "Permalink to this headline")

![_images/sensor_nxt_temp.png](_images/sensor_nxt_temp.png)

_class_ `TemperatureSensor`(_port_)[¶](#pybricks.nxtdevices.TemperatureSensor "Permalink to this definition")

LEGO® MINDSTORMS® NXT Temperature Sensor.

 

Parameters:

**port** ([_Port_](parameters.html#pybricks.parameters.Port "pybricks.parameters.Port")) – Port to which the sensor is connected.

`temperature`()[¶](#pybricks.nxtdevices.TemperatureSensor.temperature "Permalink to this definition")

Measures the temperature.

 

Returns:

Measured temperature.

Return type:

[temperature: °C](signaltypes.html#temperature)

## NXT Energy Meter[¶](#nxt-energy-meter "Permalink to this headline")

![_images/energymeter.png](_images/energymeter.png)

_class_ `EnergyMeter`(_port_)[¶](#pybricks.nxtdevices.EnergyMeter "Permalink to this definition")

LEGO® MINDSTORMS® Education NXT Energy Meter.

 

Parameters:

**port** ([_Port_](parameters.html#pybricks.parameters.Port "pybricks.parameters.Port")) – Port to which the sensor is connected.

`storage`()[¶](#pybricks.nxtdevices.EnergyMeter.storage "Permalink to this definition")

Gets the total available energy stored in the battery.

 

Returns:

Remaining stored energy.

Return type:

[energy: J](signaltypes.html#energy)

`input`()[¶](#pybricks.nxtdevices.EnergyMeter.input "Permalink to this definition")

Measures the electrical signals at the input (bottom) side of the energy meter. It measures the voltage applied to it and the current passing through it. The product of these two values is power. This power value is the rate at which the stored energy increases. This power is supplied by an energy source such as the provided solar panel or an externally driven motor.

 

Returns:

Voltage, current, and power measured at the input port.

Return type:

([voltage: mV](signaltypes.html#voltage), [current: mA](signaltypes.html#current), [power: mW](signaltypes.html#power))

`output`()[¶](#pybricks.nxtdevices.EnergyMeter.output "Permalink to this definition")

Measures the electrical signals at the output (top) side of the energy meter. It measures the voltage applied to the external load and the current passing to it. The product of these two values is power. This power value is the rate at which the stored energy decreases. This power is consumed by the load, such as a light or a motor.

 

Returns:

Voltage, current, and power measured at the output port.

Return type:

([voltage: mV](signaltypes.html#voltage), [current: mA](signaltypes.html#current), [power: mW](signaltypes.html#power))

## Vernier Adapter[¶](#vernier-adapter "Permalink to this headline")

_class_ `VernierAdapter`(_port_, _conversion=None_)[¶](#pybricks.nxtdevices.VernierAdapter "Permalink to this definition")

LEGO® MINDSTORMS® Education NXT/EV3 Adapter for Vernier Sensors.

 

Parameters:

*   **port** ([_Port_](parameters.html#pybricks.parameters.Port "pybricks.parameters.Port")) – Port to which the sensor is connected.
*   **conversion** (_callable_) – Function of the format [`conversion()`](#pybricks.nxtdevices.VernierAdapter.conversion "pybricks.nxtdevices.VernierAdapter.conversion"). This function is used to convert the raw analog voltage to the sensor-specific output value. Each Vernier Sensor has its own conversion function. The example given below demonstrates the conversion for the Surface Temperature Sensor.

`voltage`()[¶](#pybricks.nxtdevices.VernierAdapter.voltage "Permalink to this definition")

Measures the raw analog sensor voltage.

 

Returns:

Analog voltage.

Return type:

[voltage: mV](signaltypes.html#voltage)

`conversion`(_voltage_)[¶](#pybricks.nxtdevices.VernierAdapter.conversion "Permalink to this definition")

Converts the raw voltage (mV) to a sensor value.

If you did not provide a `conversion` function earlier, no conversion will be applied.

 

Parameters:

**voltage** ([voltage: mV](signaltypes.html#voltage)) – Analog sensor voltage

Returns:

Converted sensor value.

Return type:

float

`value`()[¶](#pybricks.nxtdevices.VernierAdapter.value "Permalink to this definition")

Measures the sensor [`voltage()`](#pybricks.nxtdevices.VernierAdapter.voltage "pybricks.nxtdevices.VernierAdapter.voltage") and then applies your [`conversion()`](#pybricks.nxtdevices.VernierAdapter.conversion "pybricks.nxtdevices.VernierAdapter.conversion") to give you the sensor value.

 

Returns:

Converted sensor value.

Return type:

float

**Show/hide example**

**Example: Using the Surface Temperature Sensor.**

#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Port
from pybricks.nxtdevices import VernierAdapter

from math import log

\# Conversion formula for Surface Temperature Sensor
def convert\_raw\_to\_temperature(voltage):

    \# Convert the raw voltage to the NTC resistance
    \# according to the Vernier Adapter EV3 block.
    counts \= voltage/5000\*4096
    ntc \= 15000\*(counts)/(4130\-counts)

    \# Handle log(0) safely: make sure that ntc value is positive.
    if ntc <= 0:
        ntc \= 1

    \# Apply Steinhart-Hart equation as given in the sensor documentation.
    K0 \= 1.02119e-3
    K1 \= 2.22468e-4
    K2 \= 1.33342e-7
    return 1/(K0 + K1\*log(ntc) + K2\*log(ntc)\*\*3)

\# Initialize the adapter on port 1
thermometer \= VernierAdapter(Port.S1, convert\_raw\_to\_temperature)

\# Get the measured value and print it
temp \= thermometer.value()
print(temp)