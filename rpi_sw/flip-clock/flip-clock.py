#!/usr/bin/python3

import time
from rpi_ws281x import Color
from lib import iz2k_io
from lib import iz2k_audio
from lib import iz2k_spotify
from lib import iz2k_radio
from lib import iz2k_led
from lib import iz2k_clock
from lib import iz2k_alarmclock
from lib import iz2k_config
from frontend import iz2k_frontend, config_models
from frontend.app import frontendqueue
import os

# Define CTRL callbacks
def vol_rotary_callback(direction):
	if direction is 1:
		if sound.volume_up():
			strip.colorBlinkPos(color=Color(0,50,0), pos=sound.volume/sound.volume_step)
	if direction is -1:
		if sound.volume_down():
			strip.colorBlinkPos(color=Color(0,0,50), pos=sound.volume/sound.volume_step)	

def vol_sw_short():
	print("[UI] VOL pressed SHORT")
	sound.toggle_mute()

def vol_sw_long():
	print("[UI] VOL pressed LONG")
	sound.set_volume(50)

def ctrl_rotary_callback(direction):
	global status
	print("[UI] CTRL_ROTARY:", direction)
	
	if status == 'spotify':
		sound.play('source')
		if direction == -1:
			spotify.previous_track()
		elif direction == 1:
			spotify.next_track()
	elif status == 'radio':
		sound.play('source')
		if direction == -1:
			radio.previous_station()
		elif direction == 1:
			radio.next_station()

def ctrl_sw_short():
	print("[UI] CTRL pressed SHORT")
	if status == 'spotify':
		sound.play('source')
		spotify.next_list()

def ctrl_sw_long():
	global status
	print("[UI] CTRL pressed LONG")
	if status == 'idle':
		sound.play('on')
		status='spotify'
		sound.say_text('Spotify', lang='es', wait=True)
		time.sleep(1)
		spotify.play_spotify()
	elif status == 'spotify':
		sound.play('on')
		status = 'radio'
		spotify.kill_spotify()
		sound.say_text('Radio', lang='es', wait=True)
		time.sleep(1)
		radio.play_radio()
	elif status == 'radio':
		sound.play('off')
		status = 'idle'
		radio.kill_radio()

def snooze_sw_short():
	print("[UI] SNOOZE pressed SHORT")
	alarmclock.snooze_short()
	strip.nightlight(Color(64, 5, 0))

def snooze_sw_long():
	print("[UI] SNOOZE pressed LONG")
	alarmclock.snooze_long()

def load_config():
	# Load config
	rundir = os.path.dirname(os.path.realpath(__file__))
	return config_models.load_config(rundir + '/config/config.xml')

# Set initial status
status='idle'

# Load config (credentials...)
conf = load_config()

# Create audio controler
sound = iz2k_audio.sound()

# Create spotify controller
spotify = iz2k_spotify.spotify(sound=sound, user=conf.spotify_user, pwd=conf.spotify_pass)

# Create radio controller
radio = iz2k_radio.radio(sound=sound)

# Create LED strip
strip = iz2k_led.neoled()

# Create VOL rotary
vol_rotary = iz2k_io.rotary(A=27, B=23, G=22, callback=vol_rotary_callback)

# Create VOL switch
vol_switch = iz2k_io.switch(I=24, G=25)
vol_switch.setup_switch(long_press=True, sw_short_callback=vol_sw_short, sw_long_callback=vol_sw_long)

# Create CTRL rotary
ctl_rotary = iz2k_io.rotary(A=12, B=16, G=13, callback=ctrl_rotary_callback)

# Create CTRL switch
ctrl_switch = iz2k_io.switch(I=5, G=6)
ctrl_switch.setup_switch(long_press=True, sw_short_callback=ctrl_sw_short, sw_long_callback=ctrl_sw_long)

# Create SNOOZE switch
ctrl_switch = iz2k_io.switch(I=4, G=17)
ctrl_switch.setup_switch(long_press=True, sw_short_callback=snooze_sw_short, sw_long_callback=snooze_sw_long)

# Create clock controller
clock = iz2k_clock.clock(darksky=conf.darksky_secret)

# Create alarmclock controller
alarmclock=iz2k_alarmclock.alarmclock(sound, spotify, radio, strip, clock)

# Create web frontend app
iz2k_frontend.iz2k_frontend_init()

print('Flip ClockController running!')

# Keep alive
while True:
	clock.run()
	alarmclock.run()
	time.sleep(0.5)	
	while frontendqueue.empty() is False:
		frontend_msg=frontendqueue.get()
		if frontend_msg == 'radio_update':
			radio.reload_xml()
		elif frontend_msg == 'spotify_update':
			spotify.reload_xml()
		elif frontend_msg == 'alarm_update':
			alarmclock.reload_xml()
		elif frontend_msg == 'config_update':
			conf = load_config()
			spotify.set_credentials(user=conf.spotify_user, pwd=conf.spotify_pass)
			clock.set_secret(darksky=conf.darksky_secret)
		elif frontend_msg == 'clock-calibration-on':
			clock.calibration(True)
		elif frontend_msg == 'clock-calibration-off':
			clock.calibration(False)
		elif 'clock-set' in frontend_msg:
			clock.set(frontend_msg)
		elif 'clock-sync' in frontend_msg:
			clock.sync(frontend_msg)
		elif 'clock-cal' in frontend_msg:
			clock.cal(frontend_msg)
	while alarmclock.queue.empty() is False:
		alarmclock_msg = alarmclock.queue.get()
		if alarmclock_msg == 'spotify':
			status='spotify'
		elif alarmclock_msg == 'radio':
			status='radio'
			
