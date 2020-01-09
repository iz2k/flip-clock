# Flip-Clock RPI3 A+: software design

The software in the Raspberry Pi 3 Model A+ is in charge of controlling the global funtionality of the device. It connects to the internet to get the current time, weather forecast and audio streams. All of it is performed according to the user interaction with the rotatory wheels, snooze bar and configuration files.

The software is written in Python 3 and makes use of several python libraries and external CLI applications.

## RPI3 setup

In order to run the Flip-Clock software on the Raspberry Pi 3 Model A+, the device has to be set up correctly. The software has been developed and tested on the `Raspbian Buster Lite (2019-09-26)` OS (without desktop). In any case, it should be possible to run it on other versions of Raspian.

### WPA supplicant

The first parameter to set up is the WiFi connectivity. The Model A+ does not have an ethernet connector, so the connectivity to internet is provded by WiFi. The easiest way to get the wifi connection working, is to use the WPA supplicant. Basically, you need to include a file called `wpa_supplicant.conf` in the `/etc/wpa_supplicant/` folder.

This can also be achieved connecting the SD card with Raspian to your Windows/MacOS computer and copying the `wpa_supplicant.conf` file into the FAT32 `/boot` partition. Raspian will copy the file to the correct location in the next boot (of the RPI3).

The content of the file has to be as follows:

````
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=ES

network={
	ssid="My SSID"
	psk="My Password"
	key_mgmt=WPA-PSK
}
````

You can add multiple networks if you want the device to connect to the internet in different locations.

### I2S audio (PWM)

In order to make the sound work with the Adafruit I2S 3W Stereo Speaker Bonnet, you can use the <a href="https://github.com/adafruit/Raspberry-Pi-Installer-Scripts">script on their github</a>. If you do not want to deep in in the details, just run the following curl script:

If you do not have curl already installed on your system, just do it:

````
sudo apt-get update
sudo apt-get install curl
````

And then execute the script:

````
curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh | bash
````

### UART

The UART is required to communicate with the Flip-Clock-Contorller PCB. As by default in Raspian the UART is assigned to the console, you will need to disable the console and enable the software UART `/dev/ttyS0`.

This can be easily achieved using the `raspi-config` tool. Go to the `Interfacing Options` section, and then to `Serial`.

### SPI

In order to control the NeoPixel stick, we will use the <a href="https://github.com/jgarff/rpi_ws281x">rpi_ws281x</a> python library. This library supports controlling the stick using PCM, PWM or SPI. Given that we are using PCM for audio and PWM for PiGPIO (see in dependencies), we will use the SPI for the NeoPixel stick.

Many distributions have a maximum SPI transfer of 4096 bytes. This can be changed in /boot/cmdline.txt by appending

````
spidev.bufsiz=32768
````

On the RPi 3 you have to change the GPU core frequency to 250 MHz, otherwise the SPI clock has the wrong frequency. Do this by adding the following line to /boot/config.txt and reboot.

````
core_freq=250
````

SPI requires you to be in the gpio group if you wish to control your LEDs without root.

## Dependencies

Once the hardware of the Raspberry Pi has been correctly set-up, the dependencies of the project have to be installed.

### Python 3

### PiGPIO (PWM)

<a href="http://abyz.me.uk/rpi/pigpio/index.html">PiGPIO</a> is a library for the Raspberry Pi which allows control of the General Purpose Input Outputs (GPIO). This library has been selected as it provides a fast response time, which is required for the rotary encoders.

Install the PiGPIO deamon as follows:

````
sudo apt-get update
sudo apt-get install pigpio python-pigpio python3-pigpio
````

In order to make the pigpio deamon run on startup you can either enable it via systemctl, or add a root crontab job. 

As explained in <a href="https://www.raspberrypi.org/forums/viewtopic.php?t=103752#p717150">this</a> post, use

````
sudo crontab -e
````

to edit the root crontab and add the following line to the end. Then ctrl-o return ctrl-x to exit.

````
@reboot              /usr/local/bin/pigpiod
````

### mplayer

### SoftFM

#### RTL-SDR

### Tizonia

### Raspotify (optional)

## Flip-Clock software

### Autostart (systemd unit file)

### Code structure

#### Main program

#### Libraries

##### Clock

##### Audio

##### LED

##### Encoder

##### Spotify

##### Radio

##### Alarm

#### Front-end (flask)

#### Configuration files
