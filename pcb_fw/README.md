# Flip-Clock-Controller PCB: firmware design

The firmware of the Flip-Clock-Controller PCB has been designed using Code Composer Studio. The device is controled via standard UART communication at 115200 bauds. Here are the supported commands. The commands are decoded after receiving a return character.

| Command | Description |
|--|--|
| i | Shows current situation of HH and MM digits |
| hXX | Move HH digit to poxition XX (where XX are two decimal digits) |
| mXX | Move MM digit to poxition XX (where XX are two decimal digits) |
| sh | Sync HH digit. Keeps on moving flaps until the limit switch finds the synchronization position. |
| sm | Sync MM digit. Keeps on moving flaps until the limit switch finds the synchronization position. |
| chXX | Calibrate HH value in synchronization position to XX (where XX are two decimal digits)|
| cmXX | Calibrate MM value in synchronization position to XX (where XX are two decimal digits)|

In order to add the weather forecast digit, a second Flip-Clock-Controller PCB has been used. For control simplicity, and given that the PCB echoes the received UART characters, the UART of the two PCBs have been connected in daisy-chain.

|Subpart | PIN | PIN | Subpart |
|--|--|--|--|
|RPI3 | TX | RX | Flip-Clock-Controller PCB 1 (HHMM)|
|Flip-Clock-Controller PCB 1 (HHMM) | TX | RX | Flip-Clock-Controller PCB 2 (WW)|
|Flip-Clock-Controller PCB 2 (WW) | TX | RX | RPI3|

For the second PCB, a modified version of the firmware has been used, where the following commands are included:

| Command | Description |
|--|--|
| y | Shows current situation of WW digit |
| wXX | Move WW digit to poxition XX (where XX are two decimal digits) |
| sw | Sync WW digit. Keeps on moving flaps until the limit switch finds the synchronization position. |
| cwXX | Calibrate WW value in synchronization position to XX (where XX are two decimal digits)|


## Flashing the MSP430

I have used a <a href="http://www.ti.com/tool/MSP-FET">MSP-FET</a> device as I already own one. If you do not have one, a basic <a href="http://www.ti.com/tool/MSP-EXP430FR2433?keyMatch=MSP430FR2433%20LAUNCHPAD&tisearch=Search-EN-everything">launchpad</a> can be used to program an external device. Finally, it is also possible to flash the device via the UART BSL using <a href="http://www.ti.com/tool/UNIFLASH?keyMatch=UNIFLASH&tisearch=Search-EN-everything&usecase=part-number">Uniflash</a> software.