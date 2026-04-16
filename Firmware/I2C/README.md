# I2C firmware

This folder contains the `OptDetect` Arduino library for using the Laser Lickport as an I2C-connected optical detector.

## What it does

This version is organized as a library-first Arduino package:

- `OptDetect` provides the reusable library code for communicating with the detector over I2C
- `OptDetect/examples/LaserLickport_I2C_Slave` provides the ATTiny85 example that exposes the optical reading over I2C
- `OptDetect/examples/LaserLickport_I2C_Master` provides the Arduino master example that polls the detector

The default I2C address in the current code is `0x15`.

## When to use this version

Choose this version if you:

- want to integrate the lick sensor into your own Arduino or microcontroller firmware
- want raw optical readings over I2C instead of a simple TTL output
- want a small reusable interface library with example sketches rather than a pyControl-specific workflow

This is the best fit when the lick sensor is one component inside a larger embedded system.

## Folder layout

- [`OptDetect`](./OptDetect) is the Arduino library and contains the reusable `src/` code, `library.properties`, and example sketches.
- [`OptDetect/examples/LaserLickport_I2C_Slave`](./OptDetect/examples/LaserLickport_I2C_Slave) contains the ATTiny85 example that samples the optical input on `A2` and serves the latest reading over I2C.
- [`OptDetect/examples/LaserLickport_I2C_Master`](./OptDetect/examples/LaserLickport_I2C_Master) contains the Arduino master example that connects to the detector, sets a threshold, and prints readings to the serial monitor.

## Current limitations

- The current I2C path is focused on the optical channel only.
- The slave example returns raw optical data; higher-level logic is expected to live on the master side.
- The bundled library declares `avr` in `library.properties`, so it is currently documented around AVR-style Arduino environments.

## Typical workflow

1. Add the [`OptDetect`](./OptDetect) library to your Arduino environment.
2. Start from one of the example sketches in [`OptDetect/examples`](./OptDetect/examples).
3. Flash the ATTiny85 with [`LaserLickport_I2C_Slave.ino`](./OptDetect/examples/LaserLickport_I2C_Slave/LaserLickport_I2C_Slave.ino) if you are building the detector-side firmware.
4. Use [`LaserLickport_I2C_Master.ino`](./OptDetect/examples/LaserLickport_I2C_Master/LaserLickport_I2C_Master.ino) as a reference for polling the detector from an Arduino host.
