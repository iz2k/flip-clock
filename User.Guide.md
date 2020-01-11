# Flip-Clock: User Guide

## Front buttons

![image](https://user-images.githubusercontent.com/57298545/72205597-4ae46c00-3485-11ea-8aa5-a8744997032f.png)

The main functionality of the Flip-Clock is controlled with the front buttons. 

### Contorl wheel

The control wheel is a rotary encoder with integrated switch that is used to change the operation mode of the device. Each time you make a long push to the control wheel, the operation mode will switch.

Currently this is the operation mode sequence:
* Idle
* Spotify
* Radio

#### Spotify mode

While in spotify mode use the wheel as follows:

* Move clockwise: move the spotify player to the next song.
* Move counterclockwise: move the spotify player to the previous song.
* Short press: move the spotify player to the next playlist.
* Long press: Go to radio mode.

#### Radio mode

While in radio mode use the wheel as follows:

* Move clockwise: move the radio tuner to the next station.
* Move counterclockwise: move the radio tuner to the previous station.
* Short press: TBD.
* Long press: Switch off (go to idel mode).

### Volume wheel

The volume wheel allows changing the volume of the device as follows:

* Move clockwise: increment volume (2% steps).
* Move counterclockwise: decrement volume (2% steps).
* Short press: mute/unmute.
* Long press: TBD

### Snooze bar

The snooze bar can be used in two different scenarios: whilst an alarm is operational, or not.

#### No alarm operational

* Short press: turn on the nightlight (turns off automatically after 4 seconds)

#### Alarm is operational

* Short press: snooze the alarm. If enabled, the alarm will trigger again after the configured snooze time.
* Long press: turn off the alarm. The alarm will not longer trigger after the snooze time.

## Web front-end

In addition to the front buttons, the Flip-Clock has one more interface: an integrated web front-end. This web front-end can be accessed connecting to the port 5000 of the device:

````
http://flip-clock-pi:5000
````

![image](https://user-images.githubusercontent.com/57298545/72206043-c7794980-3489-11ea-9262-f6743d16b55d.png)

### Clock

The clock fornt-end allows calibrating the Flip-Clock digits. This should be done once after manufacturing the clock. Note that whilst in calibration mode, the clock will not update with the current time.

| Clock (debug: off)  | Clock (debug: on) |
|--|--|
|![image](https://user-images.githubusercontent.com/57298545/72206010-9567e780-3489-11ea-9d63-318ae3381d44.png) | ![image](https://user-images.githubusercontent.com/57298545/72206015-9862d800-3489-11ea-9610-de942876919f.png) |

#### Clock digits calibration

In order to calibrate a digit, follow this procedure:
* Click on `Sync XX`: this will triger the selected digit to start moving until the synchronization switch is reached. The digit will stop at the synchronization position.
* Set the current value in the digit box, and click on `Cal XX`
* Set a different value in the digit box, and click on `Set XX` to test if the digit has been properly calibrated.

For the weather digit calibration, keep in mind the following number to weather icon conversion table:

| Numer | Weather icon |
|--|--|
| 01 | Clear day |
| 02 | Clear night |
| 03 | Partly cloudy day |
| 04 | Partly cloudy night |
| 05 | Cloudy |
| 06 | Fog |
| 07 | Wind |
| 08 | Sleet |
| 09 | Rain |
| 10 | Snow |

Once all three digits have been calibrated, disable the debug mode to let the clock be updated with the current time and weather.

### Alarms

The alarm front-end allows configuring the desired alarms. You can configure as many alarms as you want.

![image](https://user-images.githubusercontent.com/57298545/72206024-a3b60380-3489-11ea-8417-e94ad59e85d2.png)

The configuration parameters of the alarm are:

* Enable switch: enable/disable alarm.
* Alarm name: a name to recognize the alarm.
* Weekday switches: select to which weekdays the alarm applies.
* Alarm type: select if the alarm shall trigger the spotify player or the radio tuner.
* Alarm source: 
 * For spotify: the URI of the track or playlist to play.
 * For Radio: frequency to tune (in MHz).
* Shuffle switch: If the source is a playlist, enable/disable shuffling.
* Start volume: initial volume when the alarm triggers.
* End volume: final volume that the alarm will end up with after the specified ramp time.
* Ramp time: ram time (in minutes) for the volume ramp.
* Snooze switch: enable/disable snooze function.
* Snooze time: if enabled, time until the next alarm trigering after snooze bar has been pressed.
* Greeting switch: enable/disable greeting and weather forecast.
* Greeting text: custom text that the device will speak out loud prior to the weather forecast.
* Weather delay: delay (in minutes) from alarm trigger to weather forecast.

### Spotify

The spotify front-end allows configuring the spotify items (track/playlist) that will play in spotify mode.

![image](https://user-images.githubusercontent.com/57298545/72206028-ae709880-3489-11ea-82d1-f088251e5bce.png)

The configuration parameters of the spotify items are:

* Name: a name to recognize the item.
* Shuffle switch : enable/disable shuffling.
* URI: Spotify URI (Uniform Resource Indicator) of the item.

The URI of a spotify item can be easily found in spotify right-clicking an item.

### Radio

The radio front-end allows configuring the radio stations that will be tuned in radio mode.

![image](https://user-images.githubusercontent.com/57298545/72206031-b3354c80-3489-11ea-8725-497d57369ff0.png)

The configuration parameters of the radio stations are:

* Name: a name to recognize the item.
* Frequency : frequency (in MHZ) to be tuned.

The radio fornt-end also includes a real time radio control to tune the radio of the Flip-Clock at the desired frequency. This is useful to find the different radio stations during the configuration.

### Config

The configuration front-end allowd configuring credentials and other required values for the services such us spotify or DarkSky (for weather forecast).

![image](https://user-images.githubusercontent.com/57298545/72206039-bd574b00-3489-11ea-8f6a-097379624757.png)