#!/usr/bin/python3

import time
from rpi_ws281x import Color
from lib import iz2k_io
from lib import iz2k_audio
from lib import iz2k_radio
from lib import iz2k_led
from lib import iz2k_clock
from lib import iz2k_config

# Define CTRL callbacks
def vol_rotary_callback(direction):	
	if direction is 1:
		if sound.volume_up():
			strip.colorBlink(color=Color(0,50,0))
	if direction is -1:
		if sound.volume_down():
			strip.colorBlink(color=Color(0,0,50))	

def vol_sw_short():
	print("[UI] VOL pressed SHORT")
	sound.toggle_mute()

def vol_sw_long():
	print("[UI] VOL pressed LONG")
	sound.set_volume(50)

def ctrl_rotary_callback(direction):
	global status
	print("[UI] CTRL_ROTARY:", direction)
	
	if status == 'radio':
		sound.play('source')
		if direction == -1:
			radio.previous_station()
		elif direction == 1:
			radio.next_station()

def ctrl_sw_short():
	print("[UI] CTRL pressed SHORT")

def ctrl_sw_long():
	global status
	print("[UI] CTRL pressed LONG")
	if status == 'idle':
		sound.play('on')
		status='radio'
		radio.play_radio()
	elif status == 'radio':
		sound.play('off')
		status = 'idle'
		radio.kill_radio()

def snooze_sw_short():
	print("[UI] SNOOZE pressed SHORT")
	strip.nightlight(Color(64, 5, 0))

def snooze_sw_long():
	print("[UI] SNOOZE pressed LONG")

# Load config
#conf = iz2k_config.configuration()
status='idle'

# Create audio controler
sound = iz2k_audio.sound()

# Create radio controller
radio = iz2k_radio.radio()

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
clock = iz2k_clock.clock()

print('Flip ClockController running!')

# Keep alive
while True:
	clock.run()
	time.sleep(0.5)	
