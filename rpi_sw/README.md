# Flip-Clock RPI3 A+: software design

The software in the Raspberry Pi 3 Model A+ is in charge of controlling the global funtionality of the device. It connects to the internet to get the current time, weather forecast and audio streams. All of it is performed according to the user interaction with the rotatory wheels, snooze bar and configuration files.

The software is written in Python 3 and makes use of several python libraries and external CLI applications.

## RPI3 setup

In order to run the Flip-Clock software on the Raspberry Pi 3 Model A+, the device has to be set up correctly. The software has been developed and tested on the `Raspbian Buster Lite (2019-09-26)` OS (without desktop). In any case, it should be possible to run it on other versions of Raspian.

### WPA supplicant

The first parameter to set up is the WiFi connectivity. The Model A+ does not have an ethernet connector, so the connectivity to internet is provded by WiFi. The easiest way to get the wifi connection working, is to use the WPA supplicant. As explained in <a href="https://howchoo.com/g/ndy1zte2yjn/how-to-set-up-wifi-on-your-raspberry-pi-without-ethernet">this</a> post, you need to include a file called `wpa_supplicant.conf` in the `/etc/wpa_supplicant/` folder.

This can also be achieved connecting the SD card with Raspian to your Windows/MacOS computer and copying the `wpa_supplicant.conf` file into the FAT32 `/boot` partition. Raspian will copy the file to the correct location in the next boot of the pi.

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

Given that the Flip-Clock software is written in python, you will need the correct interpreter. Install python 3 as follows:

````
sudo apt-get install python3
````

Additionally, you will need to install several dependencies referenced in the project using `pip3`:

````
sudo pip3 install time
sudo pip3 install os
sudo pip3 install datetime
sudo pip3 install rpi_ws281x
sudo pip3 install pigpio
sudo pip3 install queue
sudo pip3 install wave
sudo pip3 install alsaaudio
sudo pip3 install subprocess
sudo pip3 install shlex
sudo pip3 install darksky
sudo pip3 install lxml 
sudo pip3 install subprocess
sudo pip3 install shlex
sudo pip3 install flask
sudo pip3 install threading
sudo pip3 install wtforms 
sudo pip3 install decimal
````

I may be missing some module. In case you get an error of some module missing, just install it using `pip3`.

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
@reboot              /usr/bin/pigpiod -t 0
````

Note that it is necessary to use the `-t 0` argument in order to launch the `pigpio` deamon in `PWM` mode instead of the default `PCM` mode. Failing to do so will break the audio that is already using the PCM hardware.

### mplayer

In order to play audio files, or in this case to play the audio returned by google translate for TTS purposes, install `mplayer`:

````
sudo apt-get install mplayer
````

### SoftFM

In order to synthonize FM radio using the RTL-SDR stick, we will use an improved version of `rtl_fm` called `softfm`. It gets better results with poor quality radio signals. We will have to build the binary for the RPI3 ourselves, but it is quite straightforward.

#### Install RTL-SDR

First install the RTL-SDR library in order to have the required header files.

````
sudo apt-get install rtl-sdr
````

You can check if the RTL-SDR usb dongle is recognized as follows:

````
rtl_test
````

Yous should see something similar to this:

````
Found 1 device(s):
  0:  Generic, RTL2832U, SN: 77771111153705700
````


#### Build SoftFM

As explained in the <a href="https://github.com/jorisvr/SoftFM">SoftFM github repository</a>, to install SoftFM, download and unpack the source code and go to the top level directory. 

First make sure you have the build tools installed:

````
sudo apt-get install libusb-1.0-0-dev
sudo apt-get install build-essential
````

Then do like this:

````
mkdir build
cd build
cmake ..

make
````

You can test if the generated binary works fine:

````
./softfm -f <radio-frequency-in-Hz>
````


### Tizonia
<a href="http://tizonia.org/">Tizonia</a> is a cloud music player from the Linux terminal. It supports some of the major cloud music services: Spotify, Google Play Music, SoundCloud, YouTube, Plex and Chromecast. We will use this CLI player to add playback support from Spotify. It should be straightforward to extend playback support for the other supported audio streaming platforms, but this has not been implemented for now, as I am currently a Spotify user.

Install Tizonia as follows:

````
curl -kL https://github.com/tizonia/tizonia-openmax-il/raw/master/tools/install.sh | bash
````

### Raspotify (optional)

Even if Tizonia is great and allows us to stream music from spotify from code, it will not show our Flip-Clock as a Spotify device in our network. If you want to use the Flip-Clock as a smart speaker that shows as a spotify device and can be controlled by your smartphone, just install Raspotify. This is optinal, as the rest of the software does not depend on raspotify to function.

To install raspotify, follow the instructions on the <a href="https://github.com/dtcooper/raspotify">Raspotify github repository</a>:

````
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
````

## Flip-Clock software

In order to run the Flip-Clock software, just copy all the files to the desired location. I used `/usr/share/flip-clock`. for ease of use, make the main file executable:

````
chmod +x flip-clock.py
````

You can also add a symbolic link to `/usr/bin` in order to make it visible to $PATH.

````
ln -s /usr/share/flip-clock/flip-clock /usr/bin/flip-clock
````

To run the software, just execute it:

````
./flip-clock
````

### Autostart (systemd unit file)

In order to make the Flip-Clock software run automatically on every boot, you can create a systemd unit file. I have included a reference unit file in the `autostart` folder.

Copy the flip-clock.service file to `/etc/systemd/system/` folder:

````
sudo cp  flip-clock.service /etc/systemd/system/ flip-clock.service
````

The reference unit file redirects the output to syslog using the method explained <a href="https://stackoverflow.com/questions/37585758/how-to-redirect-output-of-systemd-service-to-a-file">here</a>. In order to configure syslog to handle the incoming stream, copy the `flip-clock.conf` configuration file to `/etc/rsyslog.d/`

````
sudo cp flip-clock.conf /etc/rsyslog.d/
````

Now make the log file writable by syslog:

````
chown root:adm /var/log/flip-clock.log
````

Restart rsyslog:

````
sudo systemctl restart rsyslog
````

Now the stdout/stderr of flip-clock will still be available through journalctl (`sudo journalctl -u flip-clock`) but they will also be available in `/var/log/flip-clock.log`.

Reload the systemctl daemon to read the new unit file.

````
sudo systemctl daemon-reload
````

Enable the flip-clock service to run on startup:

````
sudo systemctl enable flip-clock.service
````

Run the flip-clock service without rebooting:

````
sudo systemctl start flip-clock.service
````

### Code structure

The code structure is as follows:

````
flip-clock
 >> /config/
    >> Configuration XML files.
 >> /frontend/
    >> Flask web frontend files.
 >> /lib/
    >> Project specific library files.
 >> /sounds/ 
    >> PCM format sound files.
 >> flip-clock.py
    >> Main program.
````

#### Main program

The main program generates instances of the library classes to control the different peripherals, and keeps track of the main program flow with the user interaction. The callbacks of the rotary encoders and switches as well as the frontend event queue are read in this script to obtain the desired functionality.

#### Libraries

For each peripheral a project specific library has been created.

##### Clock

The clock library gets the current time from the system, the weather forecast form the DarkSky API and handles the UART communication towards the FlipClockPCB accordingly.

##### Audio

The audio library controls the audio of the device through alsamixer. It controls the volume and allows playing simple PCM files and converting text to audio using google translate as TTS.

##### LED

The LED library controls the Neopixel sticks to generate light signaling as requested by the main program.

##### IO

The IO library handles the rotary encoders and switches.

##### Spotify

The Spotify library handles the spotify playback through Tizonia.

##### Radio

The Radio library handles the radio synthonization through SoftFM.

##### Alarm

The Alarm library handles the alarm settings to trigger the corresponding events when the time comes.

#### Front-end (flask)

The flask based web front-end allows the user to configure the clock, radio stations, spotify playlists and alarm configurations via a web browser accesible through: `http://hostname:5000`

#### Configuration files

The configuration files store the configuration of the different peripherals.
