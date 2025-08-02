# Parachute Drag Logger

Arduino-based data logger to measure parachute drag force using an HX711 load cell module. Designed for vehicle-towed tests or wind tunnel experiments.

## Features

- Logs drag force (in Newtons) to an SD card  
- Supports tare and calibration commands via serial interface  
- Saves data files with timestamp, raw sensor value, and calibrated force  

## Hardware Setup

- HX711 load cell amplifier  
- Load cell sensor (strain gauge)  
- SD card module  
- Arduino (ESP32 or compatible)  

## Serial Commands

- `tare`: Zero the scale  
- `calibrate X`: Calibrate with known weight `X` (grams)  
- `reset`: Start a new log file  

## Output

- Data logged to files named `drag_log_X.txt` with columns:

`Millis` `RawValue` `Force(N)`


## Usage Notes

- Designed for measuring drag force pulling the load cell  
- Calibration and taring needed for accurate measurements  
