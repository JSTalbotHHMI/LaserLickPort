# LaserLickPort

Minimal pyControl + ATTiny85 project for a combined optical / capacitive lick port.

## Structure

- `controls_dialogs/` custom pyControl controls dialog
- `devices/` pyControl device modules
- `tasks/` pyControl task
- `api_classes/` pyControl GUI API for live plotting
- `Sketches/` ATTiny85 Arduino sketch

## pyControl files

Set your pyControl user folders to point at this repo's:

- `controls_dialogs`
- `devices`
- `tasks`
- `api_classes`

Then upload `tasks/laser_lick_port_task.py`.

## Wiring assumptions

- pyControl board uses `Breakout_1_2` port 3 UART.
- ATTiny85 software serial uses physical pin 5 as RX and physical pin 7 as TX.
- In the sketch these are mapped as `PB0` RX and `PB2` TX.
- Optical input is `ADC2`, which Microchip maps to `PB4` on the ATtiny25/45/85 datasheet.
- Capacitive touch input is read from `PB3` using `TinyTouch`.

## Serial protocol

Board to pyControl:

- `D,optRaw=123,capRaw=456,optFlag=0,capFlag=1`

pyControl to board:

- `T,<opt_threshold>,<cap_threshold>`
- `E,<send_opt_raw>,<send_cap_raw>,<send_opt_flag>,<send_cap_flag>`

## Notes

- The live GUI window comes from `api_classes/LaserLickPort_API.py`.
- Threshold changes and stream-enable changes can be pushed while the task is running from the custom controls dialog.

## License 

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) for the full terms.