# Flip-Clock

The Flip-Clock is a self designed and built old stylish, classic alarm clock with up to date features, such as automatic time adjustment, weather forecast, FM radio or Spotify playback. The device consists of three 3D printed flip digits, a  PCB with integrated drivers for the digit controlling stepper motors and a Raspberry Pi 3 A+ with 3W speakers to run the main code.

All the mechanics and electronics are mounted within an 3D printed old stylish elegant cover. Additionally, a snoozer bar, two rotary encoders and a RGBW LED strip are included for the user interface.

![front](https://user-images.githubusercontent.com/57298545/71837757-75b27700-30b7-11ea-80a6-72005466fa5a.jpg)

# Parts

## 3D printed flip digits

Each flip digit consists on a support structure with 2 bearings. The axle is placed inside the bearings holding two flap holders. All the flaps are mounted within those flap holders. The movement of the digit is achieved with a stepper motor and two gears. An IR transmitter and an IR receiver are palced on the top and on the bottom of the flaps to detect transitions. Additionally, a limit switch is placed close to the gears to synchronize with it each turn.
![image](https://user-images.githubusercontent.com/57298545/71839513-9f6d9d00-30bb-11ea-838c-86fd38d659cb.png)
### Subparts
1. Support structure
2. Bearings
3. Axle
4. Flap holders
5. Flaps
6. Gears
7. Stepper motor
8. IR transmitter
9. IR receiver
10. Limit switch

## FlipDigitController PCB
![image](https://user-images.githubusercontent.com/57298545/71839735-2458b680-30bc-11ea-927b-b251d45d2cdc.png)
### Subparts
1. MSP430FR2433 MCU
2. INA333 comparators
3. ULN2003 drivers

## 3D printed cover
![image](https://user-images.githubusercontent.com/57298545/71839981-af39b100-30bc-11ea-9f0e-0c204987276a.png)
### Subparts
1. Top cover
2. Bottom cover
3. Front cover
4. Back cover

## Rotary encoders
![image](https://user-images.githubusercontent.com/57298545/71840053-dc865f00-30bc-11ea-91aa-834d0723d018.png) ![image](https://user-images.githubusercontent.com/57298545/71840601-eb214600-30bd-11ea-8e2c-8bffe343c412.png)

### Subparts
1. 3D printed volume wheel
2. 3D printed control wheel
3. TT EN11-HSM1AF15 Rotary Encoders


## Snooze bar

![image](https://user-images.githubusercontent.com/57298545/71840138-ffb10e80-30bc-11ea-9305-3af52d365865.png)

## NeoPixel RGBW Strip

## 3W Speakers

## FM radio tunner (RTL-SDR)

## Raspberry Pi 3 A+

## Power Supply

# Wiring
NeoPixel DIN 	>> RPI MOSI
NeoPixel 5VDC	>> 5V
NeoPixel GND	>> GND

SnoozeBar_sw0	>> RPI 4
SnoozeBar_sw1	>> RPI 17

CTRL_enc_sw0	>> RPI 5
CTRL_enc_sw1	>> RPI 6
CTRL_enc_rot0	>> RPI 12
CTRL_enc_rot1	>> RPI 16
CTRL_enc_gnd	>> RPI 13

VOL_enc_sw0	>> RPI 24
VOL_enc_sw1	>> RPI 25
VOL_enc_rot0	>> RPI 27
VOL_enc_rot1	>> RPI 23
VOL_enc_gnd	>> RPI 22