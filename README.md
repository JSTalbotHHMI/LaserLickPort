# Laser Lickport

[![GitHub Release](https://img.shields.io/github/v/release/JSTalbotHHMI/LaserLickPort.svg)](https://github.com/JSTalbotHHMI/LaserLickPort/releases)

## Library Information

- **Name:** Laser Lickport
- **License:** BSD
- **URL:** <https://github.com/JSTalbotHHMI/LaserLickPort>
- **Author:** Jeff Talbot
- **Email:** talbotj@janelia.hhmi.org

## Description

This repository contains the documentation required to order, fabricate, and operate several variations of the Janelia Laser Lickport.

The Laser Lickport was devised to be a noiseless lick detection solution for free-roaming mice and rats undergoing electrophysiology recordings. With this solution, the electronics of the sensor are moved as far from the test subjects as is needed, and the optical components of the detector do not represent a significant hindrance to the movement of the subjects.

## Quick Start

### Basic Setup

1. Clone or download this repository.
2. Build or obtain the Laser Lickport hardware described by the files in `ECAD/` and `MCAD/`.
3. Flash the ATTiny85 with the sketch in `pyControl/Sketches/LaserLickPort_ATTiny85/`.
4. Point your pyControl user folders at this repository's `pyControl/code/api_classes`, `pyControl/code/controls_dialogs`, `pyControl/code/devices`, and `pyControl/code/tasks` folders.
5. In pyControl, upload `laser_lick_port_task.py` and run it with a `Breakout_1_2` board.
6. Connect the ATTiny85 serial lines to pyControl `Breakout_1_2` Port 3 UART and provide shared power and ground.
7. Open the custom controls dialog to set optical threshold, capacitive threshold, averaging window, and which traces are shown in the live feed.

### Commands

- `laser_lick_port_task.py`
  Task used by pyControl to acquire raw sensor data, apply moving averages, and compute lick states in software.
- `laser_lick_port_controls.py`
  Custom controls dialog for changing thresholds, averaging window, and display options during a session.
- `LaserLickPort_API.py`
  Live plotting API used to display raw sensor output, thresholds, and lick-state traces.
- `LaserLickPort_ATTiny85.ino`
  ATTiny85 firmware that samples the optical and capacitive channels and streams raw data to the pyControl board over UART.

## Operation

The ATTiny85 continuously samples two channels:

- an optical sensor on `ADC2` / `PB4`
- a capacitive touch sensor on `PB3`

It streams the raw values to the pyControl board over a binary UART protocol at `57600` baud. The pyControl task then:

- applies the moving average chosen in the controls dialog
- compares the averaged values against the current thresholds
- generates `optLick` and `capLick` state traces
- updates the live GUI plots
- records the processed data to the pyControl data file when the task is run in record mode

### Capabilities

- Supports simultaneous optical and capacitive lick sensing.
- Keeps the thresholding logic on the pyControl side so thresholds can be changed live without reflashing the ATTiny85.
- Provides live plots of raw sensor output, threshold lines, and lick-state traces.
- Supports adjustable moving-average smoothing in real time from the controls dialog.
- Includes electronics, mechanical, firmware, and pyControl code in one repository.

### Limitations

- The ATTiny85 streams raw sensor values only; lick detection depends on the pyControl task being active.
- Sampling and display rate are limited by ATTiny85 acquisition time, SoftwareSerial overhead, and pyControl logging overhead.
- The pyControl integration currently targets `Breakout_1_2` Port 3 UART.
- The repository documents the current hardware and firmware revision in this project and may need adaptation for other breakout boards or microcontrollers.

### Things to Note

- The top-level repository is organized into `ECAD/`, `MCAD/`, and `pyControl/` so fabrication files and runtime code stay together.
- The pyControl-side defaults currently use an optical threshold of `700` and a capacitive threshold of `800`.
- Lick state is computed from the smoothed values, not the unsmoothed raw stream.
- The ATTiny85 firmware currently sends binary packets containing `optRaw` and `capRaw`; the pyControl task handles averaging, thresholding, and visualization.
- The project is designed around low-noise operation for electrophysiology setups where the sensing electronics must be kept away from the animal.
