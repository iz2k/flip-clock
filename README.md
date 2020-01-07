# Flip-Clock

The Flip-Clock is an old stylish, classic alarm clock with up to date features, such as automatic time adjustment, weather forecast, FM radio or Spotify playback. The device consists of three 3D printed flip digits, a  PCB with integrated drivers for the digit controlling stepper motors and a Raspberry Pi 3 A+ with 3W speakers to run the main code.

All the mechanics and electronics are mounted within an 3D printed elegant cover. Additionally, a snoozer bar, two rotary encoders and a RGBW LED strip are included for the user interface.

| ![front](https://user-images.githubusercontent.com/57298545/71914256-84f9f900-3179-11ea-8d0d-4a8aadfc6046.jpg) | ![right](https://user-images.githubusercontent.com/57298545/71914275-8b887080-3179-11ea-872b-f87635ad4661.jpg) |
| - | - |
| ![left](https://user-images.githubusercontent.com/57298545/71914270-8a574380-3179-11ea-9435-57df9337c144.jpg) | ![back](https://user-images.githubusercontent.com/57298545/71914280-8d523400-3179-11ea-8c9b-37a2da5062ca.jpg) |

# Parts

## 3D printed flip digits

Each flip digit consists of a support structure with two bearings. The axle is placed inside the bearings holding two flap holders. All the flaps are mounted within those holders. The movement of the digit is achieved with a stepper motor and two gears. An IR transmitter and an IR receiver are palced on the top and on the bottom of the flaps to detect transitions. Additionally, a limit switch is placed close to the gears to synchronize with it each turn.

### Subparts

1.Support structure
2.Bearings (<a href="https://www.amazon.es/gp/product/B07CWLGNJ5/ref=ppx_yo_dt_b_asin_title_o07_s01?ie=UTF8&psc=1">623-2RS</a>)
3.Axle
4.Flap holders
5.Flaps
6.Gears
7.Stepper motor (<a href="https://www.amazon.es/gp/product/B07LCFKJB8/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1">28BYJ-48</a>)
8.IR transmitter (<a href="https://www.amazon.es/gp/product/B07F3W2SP4/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1">IR diode</a>)
9.IR receiver (<a href="https://www.amazon.es/gp/product/B07F3W2SP4/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1">IR photodiode</a>)
10.Limit switch (<a href="https://www.amazon.es/gp/product/B07GKS9XC7/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1">CLW1093</a>)

![](https://user-images.githubusercontent.com/57298545/71909685-cfc34300-3170-11ea-8009-0059fa54a33f.png)

## FlipDigitController PCB
The FlipDigitController PCB includes a microcontroller and drivers to control the stepper motors. Additionally, the PCB also handles the IR transmitter and receiver to detect flap transitions and the limit switch for automatic synchronization of the axle. The PCB has an UART interface for the abstraction layer protocol.

The current version of the PCB can handle up to two flip digits at the same time. For the FlipClock device two units of the PCB have been used: one to control hours and minutes flaps, and another one to control weather flaps.

| Block diagram | Layout |
|--------|--------|
|![](https://user-images.githubusercontent.com/57298545/71909251-eae18300-316f-11ea-97d6-9f295ecb5744.png) | ![](https://user-images.githubusercontent.com/57298545/71839735-2458b680-30bc-11ea-927b-b251d45d2cdc.png)|

### Subparts
1. MSP430FR2433 MCU
2. INA333 comparators
3. ULN2003 drivers

## 3D printed cover
![](https://user-images.githubusercontent.com/57298545/71839981-af39b100-30bc-11ea-9f0e-0c204987276a.png)

### Subparts
1. Top cover
2. Bottom cover
3. Front cover
4. Back cover

## Rotary encoders
For the user interface two rotary encoders have been used. The used encoders can detect steps in both directions, and include a built-in switch. One of the encoders is used to control the volume (up/down/mute), whereas the other encoder controls the audio device (FM Radio/Spotify/OFF)

| Wheels | Encoders |
| --- | --- |
|![image](https://user-images.githubusercontent.com/57298545/71840053-dc865f00-30bc-11ea-91aa-834d0723d018.png)| ![image](https://user-images.githubusercontent.com/57298545/71840601-eb214600-30bd-11ea-8e2c-8bffe343c412.png)|

### Subparts
1. 3D printed volume wheel
2. 3D printed control wheel
3. TT EN11-HSM1AF15 Rotary Encoders


## Snooze bar
A snooze bar is included on top of the FlipClock device. This bar can be used to trigger the nightlight by default, or to stop/snooze the alarm when it has been triggered. Tactile switches (<a hlink="https://octopart.com/evq-q2s03w-panasonic-1199659">EVQ-Q2S03W</a>) are placed under the bar to detect when it is pressed.

| Bar | Switch |
| --- | --- |
|![image](https://user-images.githubusercontent.com/57298545/71840138-ffb10e80-30bc-11ea-9305-3af52d365865.png) | ![image](https://user-images.githubusercontent.com/57298545/71915270-ad82f280-317b-11ea-9301-1a9b3560ee06.png) |

## NeoPixel RGBW Stick


![neopixel](https://user-images.githubusercontent.com/57298545/71912677-3e56cf80-3176-11ea-8d7b-60bb79011de1.jpg | width=50%)




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