# Flip-Clock-Controller PCB: hardware design

The Flip-Clock-Controller PCB has been designed using Circuit Maker. Unluckily, there is now way to export the design to standard design formats out of their cloud. Thus, only the fabrication outputs and the documentation is included.

The Flip-Clock-Contorller PCB features a low power MSP430FR2433 microcontroller to handle the control of the flap digits. For each digit a stepper motor driver is included. The PCB also includes the analog front-end to handle the IR transmitter and receiver so that each time a flap falls down the MCU can detect it. Additionally, a limit switch is included so that every time the gear return to the initial position the MCU can detect the position and synchronize continuously to avoid number offset due to missed flap transitions (that rarely happen). The control interface of the PCB is 3.3V UART.

Even if a integrated 5V to 3.3V DCDC is included in the design, I finally decided to bypass it and use the 3.3V provided by the Raspberry Pi 3. The rest of the components are easy to solder manually with a soldering air gun.

![](https://user-images.githubusercontent.com/57298545/71909251-eae18300-316f-11ea-97d6-9f295ecb5744.png)

## Schematics

![image](https://user-images.githubusercontent.com/57298545/72004720-42552100-324c-11ea-9383-7361d34976c5.png)

## Layout

![image](https://user-images.githubusercontent.com/57298545/72004754-58fb7800-324c-11ea-8179-0f89309f8ece.png)

## 3D

![](https://user-images.githubusercontent.com/57298545/71839735-2458b680-30bc-11ea-927b-b251d45d2cdc.png)

## Fabrication outputs

The following fabrication outputs are included:
* Gerber files
* NC Drill files
* Bill Of Materials