# Bpod firmware

This folder contains the simplest Laser Lickport firmware variant in the repository.

## What it does

The sketch in [`LaserLickport_Standalone`](./LaserLickport_Standalone) reads:

- the optical sensor on `A2`
- an analog threshold on `A1`

It then drives pin `0` high when the sensor value is greater than or equal to the threshold, and low otherwise.

In other words, this version turns the lick sensor into a straightforward TTL-style output that another controller can read.

## When to use this version

Choose this version if you:

- want the smallest amount of firmware and software setup
- only need a binary lick/not-lick output
- plan to feed that signal into Bpod or another acquisition/controller system
- prefer hardware-side thresholding instead of sending raw values to a host computer

## Current limitations

- This sketch currently uses the optical channel only.
- Thresholding happens on the microcontroller, so changing behavior means changing the threshold input rather than adjusting it in host software.
- There is no built-in streaming, plotting, or capacitive-sensor support in this folder.

## Files

- [`LaserLickport_Standalone/LaserLickport_Standalone.ino`](./LaserLickport_Standalone/LaserLickport_Standalone.ino): standalone optical-threshold firmware that outputs a digital signal.
