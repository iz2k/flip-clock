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

1. Support structure
2. Bearings (<a href="https://www.amazon.es/gp/product/B07CWLGNJ5/ref=ppx_yo_dt_b_asin_title_o07_s01?ie=UTF8&psc=1">623-2RS</a>)
3. Axle
4. Flap holders
5. Flaps
6. Gears
7. Stepper motor (<a href="https://www.amazon.es/gp/product/B07LCFKJB8/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1">28BYJ-48</a>)
8. IR transmitter (<a href="https://www.amazon.es/gp/product/B07F3W2SP4/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1">IR diode</a>)
9. IR receiver (<a href="https://www.amazon.es/gp/product/B07F3W2SP4/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1">IR photodiode</a>)
10. Limit switch (<a href="https://www.amazon.es/gp/product/B07GKS9XC7/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1">CLW1093</a>)

![](https://user-images.githubusercontent.com/57298545/71909685-cfc34300-3170-11ea-8009-0059fa54a33f.png)

## FlipDigitController PCB
The FlipDigitController PCB includes a microcontroller and drivers to control the stepper motors. Additionally, the PCB also handles the IR transmitter and receiver to detect flap transitions and the limit switch for automatic synchronization of the axle. The PCB has an UART interface for the abstraction layer protocol.

The current version of the PCB can handle up to two flip digits at the same time. For the FlipClock device two units of the PCB have been used: one to control hours and minutes flaps, and another one to control weather flaps.

| Block diagram | Layout |
|--------|--------|
|![](https://user-images.githubusercontent.com/57298545/71909251-eae18300-316f-11ea-97d6-9f295ecb5744.png) | ![](https://user-images.githubusercontent.com/57298545/71839735-2458b680-30bc-11ea-927b-b251d45d2cdc.png)|

### Subparts
1. <a href="http://www.ti.com/product/MSP430FR2433">MSP430FR2433 MCU</a>
2. <a href="http://www.ti.com/product/INA333?keyMatch=INA333&tisearch=Search-EN-everything&usecase=part-number">INA333 comparators</a>
3. <a href="https://www.ti.com/product/ULN2003A?utm_source=google&utm_medium=cpc&utm_campaign=app-null-null-GPN_EN-cpc-pf-google-wwe&utm_content=ULN2003A&ds_k=ULN2003A&DCM=yes&gclid=Cj0KCQiA9dDwBRC9ARIsABbedBNLJmCuJJccQ0TU_6kyqkmjuiaOIJmoF_R1Iqcqjsfj1315j4ct5KgaAqUfEALw_wcB&gclsrc=aw.ds">ULN2003A drivers</a>

## 3D printed cover
![](https://user-images.githubusercontent.com/57298545/71839981-af39b100-30bc-11ea-9f0e-0c204987276a.png)

### Subparts
1. 3D printed top cover
2. 3D printed bottom cover
3. 3D printed front cover
4. 3D printed back cover

## Rotary encoders
For the user interface two rotary encoders have been used. The used encoders can detect steps in both directions, and include a built-in switch. One of the encoders is used to control the volume (up/down/mute), whereas the other encoder controls the audio device (FM Radio/Spotify/OFF)

| Wheels | Encoders |
| --- | --- |
|![image](https://user-images.githubusercontent.com/57298545/71840053-dc865f00-30bc-11ea-91aa-834d0723d018.png)| ![image](https://user-images.githubusercontent.com/57298545/71840601-eb214600-30bd-11ea-8e2c-8bffe343c412.png)|

### Subparts
1. 3D printed volume wheel
2. 3D printed control wheel
3. <a href="https://www.mouser.es/ProductDetail/BI-Technologies-TT-Electronics/EN11-HSM1AF15?qs=u1MaZ2%2F4xgsleMatSs8Sqg==">TT EN11-HSM1AF15</a> Rotary Encoders


## Snooze bar
A snooze bar is included on top of the FlipClock device. This bar can be used to trigger the nightlight by default, or to stop/snooze the alarm when it has been triggered. Tactile switches are placed under the bar to detect when it is pressed.

| Bar | Switch |
| --- | --- |
|![bar](https://user-images.githubusercontent.com/57298545/71840138-ffb10e80-30bc-11ea-9305-3af52d365865.png) | ![switch](https://user-images.githubusercontent.com/57298545/71915944-1f0f7080-317d-11ea-9247-6284e7399dad.png)


### Subparts
1. 3D printed snooze bar
2. <a hlink="https://octopart.com/evq-q2s03w-panasonic-1199659">EVQ-Q2S03W</a> tactile switches


## NeoPixel RGBW Stick
Two NeoPixel RGBW LED sticks have been included in the front of the FlipClock in order to provide nightlight and light-sign functions to the device.

![neopixel](https://user-images.githubusercontent.com/57298545/71915786-c5a74180-317c-11ea-8382-9a2c862fb766.png)

### Subparts
1. <a href="https://www.adafruit.com/product/2868">NeoPixel RGBW Stick</a>




## 3W Speakers
![image](https://user-images.githubusercontent.com/57298545/71917028-78789f00-317f-11ea-9d36-5b1e801ca90e.png)

### Subparts
1. <a href="https://www.adafruit.com/product/1669">Stereo Enclosed Speaker Set - 3W 4 Ohm</a>

## FM radio tunner (RTL-SDR)

| RTL-SDR dongle | FM antenna |
| --- | --- |
|![image](https://user-images.githubusercontent.com/57298545/71916693-ca6cf500-317e-11ea-9ba9-f5a19fb1d1fc.png)|![image](https://user-images.githubusercontent.com/57298545/71916614-9db8dd80-317e-11ea-92c9-331ff1a74de6.png)|

### Subparts
1. <a href="https://www.amazon.es/gp/product/B013Q94CT6/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&psc=1">RTL-SDR dongle</a>
2. <a href="https://www.amazon.es/gp/product/B07CJYRWXQ/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1">FM antenna</a>


## Raspberry Pi 3 A+
|Raspberry Pi 3 Model A+|Adafruit I2S 3W Stereo Speaker Bonnet|
|--|--|
|![image](https://user-images.githubusercontent.com/57298545/71917662-da85d400-3180-11ea-85ec-e5f024e5f510.png)|![image](https://user-images.githubusercontent.com/57298545/71917730-0dc86300-3181-11ea-9dab-7e09cda9c585.png)|

### Subparts
1. <a href="https://www.raspberrypi.org/products/raspberry-pi-3-model-a-plus/">RPI3 A+</a>
2. <a href="https://www.adafruit.com/product/3346">Adafruit I2S 3W Stereo Speaker Bonnet</a>


## Power Supply
|Power Supply Module| PSM Housing|
|--|--|
|![image](https://user-images.githubusercontent.com/57298545/71917384-37cd5580-3180-11ea-8340-a72870a0f2ce.png)|![image](https://user-images.githubusercontent.com/57298545/71917600-bcb86f00-3180-11ea-9bb1-ffbf252b2a0e.png)|

### Subparts
1. <a href="https://www.digikey.com/product-detail/en/mean-well-usa-inc/PS-05-5/1866-5411-ND/7705819">PS-05-5</a> power supply module
2. 3D printed housing

# Wiring

The correct wiring to connect the different electronics is as follows:

PSM connection:

| Subpart | PIN | PIN | Subpart |
| -- | -- | -- | --|
| RPI3 | 5V | 5V | PSM |
| RPI3 | GND | GND | PSM |

NeoPixel connection:

| Subpart | PIN | PIN | Subpart |
| -- | -- | -- | --|
| NeoPixel | DIN | MOSI | RPI3 |
| NeoPixel | 5VDC | 5V | RPI3 |
| NeoPixel | GND | GND | RPI3 |

Snooze Bar connection:


| Subpart | PIN | PIN | Subpart |
| -- | -- | -- | --|
| Snooze Bar | SW0 | GPIO 4 | RPI3 |
| Snooze Bar | SW1 | GPIO 17 | RPI3 |

Volume Encoder<sup>1</sup> connection:


| Subpart | PIN | PIN | Subpart |
| -- | -- | -- | --|
| Volume Encoder | SW0 | GPIO 24 | RPI3 |
| Volume Encoder | SW1 | GPIO 25 | RPI3 |
| Volume Encoder | ROT0 | GPIO 27 | RPI3 |
| Volume Encoder | ROT1 | GPIO 23 | RPI3 |
| Volume Encoder | GND | GPIO 22 | RPI3 |

Control Encoder<sup>1</sup> connection:

| Subpart | PIN | PIN | Subpart |
| -- | -- | -- | --|
| Control Encoder | SW0 | GPIO 5 | RPI3 |
| Control Encoder | SW1 | GPIO 6 | RPI3 |
| Control Encoder | ROT0 | GPIO 12 | RPI3 |
| Control Encoder | ROT1 | GPIO 16 | RPI3 |
| Control Encoder | GND | GPIO 13 | RPI3 |

1: For ease of connectivity, all pins of rotary encoders are routed to GPIOs. These GPIOs will be configured as required with pull resistors or fixed voltages via software.