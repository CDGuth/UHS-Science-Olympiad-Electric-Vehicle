# GitHub Copilot Instructions

## Terminal Enviornment
PowerShell, so use powershell syntax for any terminal commands.

## Project Description
This project contains contains the program for the UHS's  Science Olympiad 2026 Electric Vehicle event device. The vehicle is built using LEGO MINDSTORMS EV3 components and programmed using the EV3 MicroPython library (Pybricks). The goal of the vehicle is to autonomously travel a specified distance and stop as close as possible to a target point as close to a given target time as possible, while adhering to event constraints.

## Event Description
The objective is to design and build a vehicle that travels a specific Target Distance and stops as close as possible to a Target Point within a Target Time.
- **Constraints**: 
  - Max 8 AA batteries (No Lithium/Lead-Acid).
  - Max Length: 70.0 cm, Max Width: 35.0 cm.
  - Must be started with a #2 pencil (ideally by pressing a button). Autonomous only.
- **Scoring**:
  - **Final Score**: Better of the 2 Run Scores + Final Score Penalties. Low score wins.
  - **Run Score**: 100 + Distance Score + Time Score + Bonuses + Run Penalties.
  - **Distance Score**: 2.0 pts/cm x Vehicle Distance error. (Failed Run = 2500 pts).
  - **Time Score**: abs(Target Time - Run Time) (Failed Run = 0.00s).
  - **Can Bonus**: -0.5 x (110 - Inside Can Distance).
  - **Run Penalties**:
    - Competition Violation: 150 points.
    - Construction Violation: 300 points.
  - **Final Score Penalties**:
    - Vehicle not Impounded: 5000 points.
  - **Tiebreakers**:
    1. Better Vehicle Distance of the scored run.
    2. Lower Time Score of the scored run.
    3. Better Vehicle Distance of the non-scored run.
    4. Better Time Score of the non-scored run.

## Track Setup
The track is on a smooth, level, hard surface.
- **Start Point**: 5x2.5 cm tape marking the center.
- **Target Point**: 5x2.5 cm tape at a distance of **7.0 to 10.0 meters** from start.
- **Imaginary Center Line**: Connects Start and Target points.
- **Bonus Line**: Tape placed **halfway** between Start and Target, extending perpendicular to the left.
- **Bonus Cans**: Two cans placed on the Bonus Line.
  - **Outer Can**: Placed by Event Supervisor exactly one meter perpendicular to the center line.
  - **Inner Can**: Placed by the team along the Bonus Line (ideally close to the outer can to maximize bonus).
  - Vehicle must pass between these cans to earn the bonus.

## Hardware Configuration
The vehicle follows a standard car design with the following components:
- **Drive System**: Two Large EV3 Motors driving the rear wheels.
- **Steering System**: One Medium EV3 Motor controlling the front steering angle.
- **Sensors**: One EV3 GyroSensor for real-time feedback and control loops.
- **Transmission**: Gear multiplier on rear wheels to increase maximum speed.

## EV3 MicroPython API Reference

### Hubs (`pybricks.hubs`)

#### `class EV3Brick`
The programmable brick.
- **`buttons.pressed()`**: Checks which buttons are currently pressed. Returns list of `Button`.
- **`light.on(color)`**: Turns on the light at the specified `Color`.
- **`light.off()`**: Turns off the light.
- **`speaker.beep(frequency=500, duration=100)`**: Play a beep/tone.
- **`speaker.play_notes(notes, tempo=120)`**: Plays a sequence of musical notes (e.g., `['C4/4', 'G4/4']`).
- **`speaker.play_file(file_name)`**: Plays a sound file (WAV).
- **`speaker.say(text)`**: Says a given text string.
- **`speaker.set_speech_options(language=None, voice=None, speed=None, pitch=None)`**: Configures speech settings.

### EV3 Devices (`pybricks.ev3devices`)

#### `class Motor(port, positive_direction=Direction.CLOCKWISE, gears=None)`
Generic class to control motors with built-in rotation sensors.
- **`speed()`**: Gets the speed of the motor (deg/s).
- **`angle()`**: Gets the rotation angle of the motor (deg).
- **`reset_angle(angle)`**: Sets the accumulated rotation angle to a desired value.
- **`stop()`**: Stops the motor and lets it spin freely (coast).
- **`brake()`**: Passively brakes the motor.
- **`hold()`**: Stops the motor and actively holds it at its current angle.
- **`run(speed)`**: Runs the motor at a constant speed (deg/s).
- **`run_time(speed, time, then=Stop.HOLD, wait=True)`**: Runs at constant speed for `time` ms.
- **`run_angle(speed, rotation_angle, then=Stop.HOLD, wait=True)`**: Runs at constant speed by a relative `rotation_angle`.
- **`run_target(speed, target_angle, then=Stop.HOLD, wait=True)`**: Runs at constant speed towards an absolute `target_angle`.
- **`run_until_stalled(speed, then=Stop.COAST, duty_limit=None)`**: Runs at constant speed until stalled. Returns stall angle.
- **`dc(duty)`**: Rotates the motor at a given duty cycle (-100 to 100).
- **`track_target(target_angle)`**: Tracks a target angle as fast as possible (no smooth accel).
- **`control`**: Access to the `Control` class to adjust PID settings.

#### `class GyroSensor(port, positive_direction=Direction.CLOCKWISE)`
LEGO MINDSTORMS EV3 Gyro Sensor.
- **`speed()`**: Gets the angular velocity of the sensor (deg/s).
- **`angle()`**: Gets the accumulated angle of the sensor (deg).
- **`reset_angle(angle)`**: Sets the rotation angle of the sensor to a desired value.

### Parameters (`pybricks.parameters`)

- **`Port`**: 
  - Motors: `Port.A`, `Port.B`, `Port.C`, `Port.D`
  - Sensors: `Port.S1`, `Port.S2`, `Port.S3`, `Port.S4`
- **`Direction`**: `Direction.CLOCKWISE`, `Direction.COUNTERCLOCKWISE`
- **`Stop`**: 
  - `Stop.COAST`: Let the motor move freely.
  - `Stop.BRAKE`: Passively resist small external forces.
  - `Stop.HOLD`: Keep controlling the motor to hold its angle.
- **`Color`**: `BLACK`, `BLUE`, `GREEN`, `YELLOW`, `RED`, `WHITE`, `BROWN`, `ORANGE`, `PURPLE`.
- **`Button`**: `LEFT_DOWN`, `DOWN`, `RIGHT_DOWN`, `LEFT`, `CENTER`, `RIGHT`, `LEFT_UP`, `UP`, `BEACON`, `RIGHT_UP`.

### Tools (`pybricks.tools`)

- **`wait(time)`**: Pauses the user program for `time` milliseconds.
- **`class StopWatch`**:
  - **`time()`**: Gets the current time (ms).
  - **`pause()`**: Pauses the stopwatch.
  - **`resume()`**: Resumes the stopwatch.
  - **`reset()`**: Resets the stopwatch time to 0.
- **`class DataLog(*headers, name='log', timestamp=True, extension='csv', append=False)`**:
  - **`log(*values)`**: Saves one or more values on a new line in the file.

### Robotics (`pybricks.robotics`)

#### `class DriveBase(left_motor, right_motor, wheel_diameter, axle_track)`
A robotic vehicle with two powered wheels.
- **`straight(distance)`**: Drives straight for `distance` mm.
- **`turn(angle)`**: Turns in place by `angle` degrees.
- **`settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration)`**: Configures default speed/accel.
- **`drive(drive_speed, turn_rate)`**: Starts driving at specified speed (mm/s) and turn rate (deg/s) forever.
- **`stop()`**: Stops the robot.
- **`distance()`**: Gets the estimated driven distance (mm).
- **`angle()`**: Gets the estimated rotation angle (deg).
- **`state()`**: Returns tuple (`distance`, `drive_speed`, `angle`, `turn_rate`).
- **`reset()`**: Resets estimated distance and angle to 0.
- **`distance_control`**: Access `Control` object for distance PID.
- **`heading_control`**: Access `Control` object for heading PID.

### Media (`pybricks.media.ev3dev`)

#### `class ImageFile`
- `ACCEPT`, `BACKWARD`, `DECLINE`, `FORWARD`, `LEFT`, `NO_GO`, `QUESTION_MARK`, `RIGHT`, `STOP_1`, `STOP_2`, `THUMBS_DOWN`, `THUMBS_UP`, `WARNING`
- `EV3`, `EV3_ICON`
- `TARGET`
- `ANGRY`, `AWAKE`, `BOTTOM_LEFT`, `BOTTOM_RIGHT`, `CRAZY_1`, `CRAZY_2`, `DIZZY`, `DOWN`, `EVIL`, `KNOCKED_OUT`, `MIDDLE_LEFT`, `MIDDLE_RIGHT`, `NEUTRAL`, `PINCHED_LEFT`, `PINCHED_MIDDLE`, `PINCHED_RIGHT`, `SLEEPING`, `TIRED_LEFT`, `TIRED_MIDDLE`, `TIRED_RIGHT`, `UP`, `WINKING`

#### `class SoundFile`
- `BOING`, `BOO`, `CHEERING`, `CRUNCHING`, `CRYING`, `FANFARE`, `KUNG_FU`, `LAUGHING_1`, `LAUGHING_2`, `MAGIC_WAND`, `OUCH`, `SHOUTING`, `SMACK`, `SNEEZING`, `SNORING`, `UH_OH`
- `ACTIVATE`, `ANALYZE`, `BACKWARDS`

### Control (`pybricks._common.Control`)
Class to interact with PID controller and settings. Accessed via `.control` attribute of motors or drivebases.
- **`scale`**: Scaling factor between controlled variable and physical output.
- **`done()`**: Checks if an ongoing command is done. Returns `bool`.
- **`stalled()`**: Checks if controller is stalled. Returns `bool`.
- **`limits(speed, acceleration, actuation)`**: Configures max speed, acceleration, and actuation.
- **`pid(kp, ki, kd, integral_range, integral_rate, feed_forward)`**: Gets or sets PID values.
- **`target_tolerances(speed, position)`**: Gets or sets tolerances for completion.
- **`stall_tolerances(speed, time)`**: Gets or sets stalling tolerances.

## Tool Use Best Practices

### File Operations
- **`read_file`**: Read large chunks (approx. 500 lines) to minimize tool calls. Use for understanding existing logic.
- **`replace_string_in_file`**: Provide EXACT matches including whitespace. Include 3 lines of context before and after the change for stability.
- **`create_file`**: Use only for NEW files. If a file exists, use an edit tool.

### Terminal & Execution
- **`run_in_terminal`**: Use for git commands, running tests, or small script executions. Prefer PowerShell cmdlets on Windows.
- **`configure_python_environment`**: Always call before using python tools. Use the project root if unsure.

### Planning & Tracking
- **`manage_todo_list`**: ALWAYS initialize a todo list for multi-step tasks. Mark items as `in-progress` before working and `completed` immediately after.

### Coding Standards
- **Configuration**: NO MAGIC NUMBERS. All configurable values (constants, loop times, physical parameters) must be defined in `config.py` and imported.
- **MicroPython**: Remember this is MicroPython on EV3. Resources are limited.

## Documentation & References

### EV3 MicroPython Documentation
**Location:** `.github/docs/EV3 MicroPython/`
**Description:** Contains comprehensive Markdown documentation for the EV3 MicroPython library (Pybricks), including the `ev3devices`, `parameters`, `robotics` modules, and more. Refer to this folder for detailed API signatures and usage examples.

### Event References
- **Event Rules:** `.github/docs/Science_Olympiad_2026_Electric_Vehicle_Rules.md` 
  *(Contains official rules, parameters, construction limits, and penalty details)*
- **Track Setup:** `.github/docs/Science_Olympiad_2026_Electric_Vehicle_Track_Setup.png`
  *(Visual diagram of the bonus line, cans, start point, and target point)*
