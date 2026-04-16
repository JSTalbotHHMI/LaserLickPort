# I2C firmware

This folder contains the I2C-based Laser Lickport implementation.

## What it does

This version splits the project into two parts:

- an ATTiny85 I2C slave that continuously reads the optical sensor and exposes the latest 16-bit value over I2C
- an Arduino-side `OptDetect` library plus a simple master example for polling that slave

The default I2C address in the current code is `0x15`.

## When to use this version

Choose this version if you:

- want to integrate the lick sensor into your own Arduino or microcontroller firmware
- want raw optical readings over I2C instead of a simple TTL output
- want a small reusable interface library rather than a pyControl-specific workflow

This is the best fit when the lick sensor is one component inside a larger embedded system.

## Folder layout

- [`LaserLickport_I2C_Slave`](./LaserLickport_I2C_Slave) contains the ATTiny85 firmware that samples the optical input on `A2` and serves the latest reading over I2C.
- [`LaserLickport_I2C_Master`](./LaserLickport_I2C_Master) contains a simple master sketch that connects to the detector, sets a threshold, and prints readings to the serial monitor.
- [`OptDetect`](./OptDetect) is an Arduino library that wraps the I2C communication and provides helper functions such as `begin()`, `isConnected()`, `getOpt()`, and `isDetected()`.
- [`OptDetect/examples/OptDetect_SerialMonitor`](./OptDetect/examples/OptDetect_SerialMonitor) contains a minimal example that prints raw readings and thresholded detection state to the serial monitor.

## Current limitations

- The current I2C path is focused on the optical channel only.
- The slave sketch returns raw optical data; higher-level logic is expected to live on the master side.
- The bundled library declares `avr` in `library.properties`, so it is currently documented around AVR-style Arduino environments.

## Typical workflow

1. Flash the ATTiny85 with [`LaserLickport_I2C_Slave.ino`](./LaserLickport_I2C_Slave/LaserLickport_I2C_Slave.ino).
2. Add the [`OptDetect`](./OptDetect) library to your Arduino environment.
3. Use the master example as a starting point, or call the library from your own code to poll the detector over I2C.
