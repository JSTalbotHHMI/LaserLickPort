# Laser Lickport

[![GitHub Release](https://img.shields.io/github/v/release/JSTalbotHHMI/LaserLickPort.svg)](https://github.com/JSTalbotHHMI/LaserLickPort/releases)

## Library Information

- **Name:** Laser Lickport
- **License:** BSD
- **URL:** <https://github.com/JSTalbotHHMI/LaserLickPort>
- **Author:** Jeff Talbot
- **Email:** talbotj@janelia.hhmi.org

## Description

This repository contains the files needed to fabricate and use several versions of the Janelia Laser Lickport.

The Laser Lickport was developed as a noiseless lick detection solution for free-roaming mice and rats, especially in electrophysiology setups where the sensing electronics need to be kept away from the animal.

## Repository layout

- [`ECAD/`](./ECAD) contains electronics design files.
- [`MCAD/`](./MCAD) contains mechanical design files.
- [`Firmware/`](./Firmware) contains the available firmware workflows for `pyControl`, `Bpod`, and `I2C`.

## Choosing a firmware path

The repository currently supports three different usage patterns:

- [`Firmware/pyControl`](./Firmware/pyControl) is the most complete integration and supports optical plus capacitive sensing, live threshold updates, smoothing, and plotting.
- [`Firmware/Bpod`](./Firmware/Bpod) is the simplest path and provides a TTL-style output from a standalone optical-threshold sketch.
- [`Firmware/I2C`](./Firmware/I2C) provides the `OptDetect` Arduino library, with detector-side and host-side example sketches under `OptDetect/examples`.

If you are not sure where to start, begin with [`Firmware/README.md`](./Firmware/README.md).

## Quick start

1. Clone or download this repository.
2. Build or obtain the Laser Lickport hardware described in [`ECAD/`](./ECAD) and [`MCAD/`](./MCAD).
3. Choose the firmware path that matches your controller and workflow.
4. Follow the README in that firmware subfolder for setup details.

## pyControl path

Choose [`Firmware/pyControl`](./Firmware/pyControl) if you want the richest software integration.

This path currently includes:

- ATTiny85 firmware that streams optical and capacitive raw values over UART
- a pyControl task
- a custom controls dialog
- a live plotting API
- pyControl device definitions

Use this option when you want live threshold tuning, smoothing, session logging, and visualization.

## Bpod path

Choose [`Firmware/Bpod`](./Firmware/Bpod) if you want the simplest microcontroller-side implementation.

This path currently includes a standalone sketch that:

- reads the optical channel on `A2`
- reads a threshold on `A1`
- drives a digital output on pin `0`

Use this option when you only need a binary lick signal for another controller.

## I2C path

Choose [`Firmware/I2C`](./Firmware/I2C) if you want to integrate the sensor into your own embedded firmware over I2C.

This path currently includes:

- the [`OptDetect`](./Firmware/I2C/OptDetect) Arduino library
- a detector-side example sketch in [`Firmware/I2C/OptDetect/examples/LaserLickport_I2C_Slave`](./Firmware/I2C/OptDetect/examples/LaserLickport_I2C_Slave)
- a host-side example sketch in [`Firmware/I2C/OptDetect/examples/LaserLickport_I2C_Master`](./Firmware/I2C/OptDetect/examples/LaserLickport_I2C_Master)

Use this option when the lick sensor is one part of a larger Arduino or microcontroller system.

## Notes

- The current `pyControl` implementation supports both optical and capacitive sensing.
- The current `Bpod` and `I2C` implementations are focused on the optical channel.
- Thresholding is handled in different places depending on the firmware path, so behavior and flexibility differ by workflow.

## Versioning

Version tracking in this repository now uses two layers:

- Repo-wide releases are tracked with Git tags such as `v0.1.0`.
- Firmware and library components are tracked in [`versions.toml`](./versions.toml).

For firmware components, the current version is also declared inside the shipped sketches so a flashed build can be traced back to source more easily:

- [`Firmware/pyControl/LaserLickport_PyControl/LaserLickport_pyControl.ino`](./Firmware/pyControl/LaserLickport_PyControl/LaserLickport_pyControl.ino)
- [`Firmware/Bpod/LaserLickport_Standalone/LaserLickport_Standalone.ino`](./Firmware/Bpod/LaserLickport_Standalone/LaserLickport_Standalone.ino)
- [`Firmware/I2C/OptDetect/examples/LaserLickport_I2C_Slave/LaserLickport_I2C_Slave.ino`](./Firmware/I2C/OptDetect/examples/LaserLickport_I2C_Slave/LaserLickport_I2C_Slave.ino)
- [`Firmware/I2C/OptDetect/examples/LaserLickport_I2C_Master/LaserLickport_I2C_Master.ino`](./Firmware/I2C/OptDetect/examples/LaserLickport_I2C_Master/LaserLickport_I2C_Master.ino)

Suggested bump rules:

- bump the repo tag when publishing a new overall release
- bump a sketch version when its behavior, pin assumptions, defaults, or compatibility change
- bump a protocol version only when the on-wire format changes
- keep the `OptDetect` library version in [`library.properties`](./Firmware/I2C/OptDetect/library.properties) aligned with library changes
