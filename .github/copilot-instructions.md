# GitHub Copilot Instructions

## Project Overview
This project is for the Science Olympiad 2026 "Electric Vehicle" event. The goal is to design an autonomous vehicle that travels a specific distance using electrical energy and stops as close as possible to a Target Point.

## Hardware Configuration
The vehicle follows a standard car design with the following components:
- **Drive System**: Two Large EV3 Motors driving the rear wheels.
- **Steering System**: One Medium EV3 Motor controlling the front steering angle.
- **Sensors**: One EV3 GyroSensor for real-time feedback and control loops.
- **Transmission**: Gear multiplier on rear wheels to increase maximum speed.

## Key EV3 MicroPython APIs
The project uses the `pybricks` library. Below are the essential classes and methods for this specific hardware configuration.

### Imports
```python
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
```

### Motor Control (Rear Drive & Front Steering)
```python
# Initialize Motors
# Adjust Port.A/B/C/D and Direction based on physical wiring
# Note: Ensure the ports match your physical connections.
left_drive = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
right_drive = Motor(Port.C, positive_direction=Direction.CLOCKWISE)
steering_motor = Motor(Port.A, positive_direction=Direction.CLOCKWISE)

# Drive Motors (Speed control)
# Differential drive logic if needed, or synchronized speed
speed_deg_s = 500
left_drive.run(speed_deg_s)
right_drive.run(speed_deg_s)

# Stopping
left_drive.stop()
left_drive.brake()
left_drive.hold()

# Steering Motor (Position control)
# Use run_target for precise angle control
steering_center_angle = 0 # Calibrated 0
steering_motor.reset_angle(0)
steering_motor.run_target(speed=500, target_angle=30, then=Stop.HOLD)
current_steer_angle = steering_motor.angle()
```

### GyroSensor
```python
# Initialize Gyro
gyro = GyroSensor(Port.S1)

# Usage
# Avoiding drift: Reset angle when stationary
gyro.reset_angle(0)
current_heading = gyro.angle() # Positive = clockwise (depending on mount)
current_rate = gyro.speed()    # Angular velocity
```

## Documentation & References

### EV3 MicroPython Documentation
**Location:** `.github/docs/EV3 MicroPython/`
**Description:** Contains comprehensive Markdown documentation for the EV3 MicroPython library (Pybricks), including the `ev3devices`, `parameters`, `robotics` modules, and more. Refer to this folder for detailed API signatures and usage examples.

### Event References
- **Event Rules:** `.github/docs/Science_Olympiad_2026_Electric_Vehicle_Rules.md` 
  *(Contains official rules, parameters, construction limits, and penalty details)*
- **Track Setup:** `.github/docs/Science_Olympiad_2026_Electric_Vehicle_Track_Setup.png`
  *(Visual diagram of the bonus line, cans, start point, and target point)*
