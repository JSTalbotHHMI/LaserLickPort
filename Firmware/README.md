# Firmware

This folder contains three different ways to use the Laser Lickport hardware.

## Which one should I choose?

### Choose `pyControl` if:

- You are already running experiments with pyControl.
- You want the most complete integration in this repository.
- You want both optical and capacitive sensing.
- You want live threshold adjustment, smoothing, and plotting during a session.

This is the richest and best-documented option in the current repository.

### Choose `Bpod` if:

- You want the simplest firmware path.
- You only need a digital lick signal that can be read by another controller such as Bpod.
- You are happy doing thresholding directly on the microcontroller instead of in host software.

The current `Bpod` sketch is a small standalone optical detector. It reads the sensor on `A2`, reads a threshold on `A1`, and drives a TTL output on pin `0`.

### Choose `I2C` if:

- You want to integrate the lick sensor into your own Arduino or microcontroller project.
- You want to read the sensor over an I2C bus instead of using a direct TTL output or pyControl UART link.
- You want a reusable Arduino library with example sketches for the detector.

The current `I2C` implementation is centered on the `OptDetect` library and is focused on the optical sensor channel.

## Quick comparison

| Option | Best for | Sensor channels in current code | Interface style |
| --- | --- | --- | --- |
| `pyControl` | Full experiment integration | Optical + capacitive | UART stream to pyControl |
| `Bpod` | Simple lick/no-lick output | Optical | TTL output |
| `I2C` | Custom embedded integrations | Optical | I2C slave + Arduino library |

## Folder contents

- [`pyControl`](./pyControl) contains the pyControl task, device files, GUI API, controls dialog, and ATTiny85 firmware.
- [`Bpod`](./Bpod) contains a standalone threshold-to-TTL sketch suitable for simple controller input workflows.
- [`I2C`](./I2C) contains the `OptDetect` Arduino library plus master and slave example sketches under `OptDetect/examples`.

## Recommendation

If you are unsure where to start, start with [`pyControl`](./pyControl). It currently exposes the most functionality and is the path in this repository with the clearest end-to-end workflow.
