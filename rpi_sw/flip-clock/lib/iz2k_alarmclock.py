from frontend import alarm_models
import os
from datetime import datetime
import time
from rpi_ws281x import Color
from queue import Queue

def currentseconds():
	now=datetime.now()
	return time.mktime(now.timetuple())


class alarmclock:

	def __init__(self, sound, spotify, radio, strip, clock):
		self.sound = sound
		self.spotify = spotify
		self.radio = radio
		self.strip = strip
		self.clock = clock
		self.queue = Queue()
		self.reload_xml()

	def reload_xml(self):
		print('[alarm] Loading alarm list')
		# Load alarms from XML
		bindir = os.path.dirname(os.path.realpath(__file__))
		self.alarms = alarm_models.load_alarm_list(bindir + '/../config/alarms.xml')
	
	def snooze_short(self):
		# Go through all alarms
		for alarm in self.alarms:
			# Check alarm is ON
			if alarm.status == 'on' or alarm.status == 'snooze_on':
				# Go silent
				self.radio.kill_radio()
				self.spotify.kill_spotify()
				if alarm.snooze.enable:
					print('[alarm] Alarm ' + alarm.name + ' going to snooze wait mode')
					alarm.status = 'snooze_wait'
					# Calculate Snooze time
					alarm.snooze.timestamp = currentseconds() + alarm.snooze.time*60
				else:
					print('[alarm] Alarm ' + alarm.name + ' going off')
					alarm.status = 'off'

	def snooze_long(self):
		# Go through all alarms
		for alarm in self.alarms:
			# Check alarm is ON or in SNOOZE wait
			if alarm.status == 'on' or alarm.status == 'snooze_on' or alarm.status == 'snooze_wait':
				# Go silent
				self.radio.kill_radio()
				self.spotify.kill_spotify()
				print('[alarm] Alarm ' + alarm.name + ' going off')
				alarm.status = 'off'
				self.sound.play('off')
				# Put light OFF		
				self.strip.colorWipe(Color(0, 0, 0))

	def play(self, alarm):
		# Set volume start volume
		alarm.volume.current = alarm.volume.start
		self.sound.set_volume(alarm.volume.current)
		# Set timestamps
		current_timestamp = currentseconds()
		alarm.volume.tstart = current_timestamp
		alarm.volume.tstop = current_timestamp + alarm.volume.ramptime*60
		alarm.weather.timestamp = current_timestamp + alarm.weather.delay*60
		# Reset flags
		alarm.weather.executed = False
		# Determine source
		if alarm.source.type=='spotify':
			print('[alarm] Alarm ' + alarm.name + ' triggered! (spotify)')
			# Kill previous playbacks if exist
			self.radio.kill_radio()
			self.spotify.kill_spotify()
			self.spotify.play_URI(URI=alarm.source.item, shuffle=alarm.source.randomize)
			self.queue.put('spotify')
		elif alarm.source.type=='radio':
			print('[alarm] Alarm ' + alarm.name + ' triggered! (radio)')
			# Kill previous playbacks if exist
			self.radio.kill_radio()
			self.spotify.kill_spotify()
			self.radio.tune_freq(freq=alarm.source.item)
			self.queue.put('radio')
		
		# Put light ON		
		self.strip.colorWipe(Color(30, 5, 0))

	def run(self):
		now = datetime.now()
		hh = now.hour
		mm = now.minute
		wd = now.weekday()
		current_timestamp = currentseconds()
		# Go through all alarms
		for alarm in self.alarms:
			# Check alarm is enabled
			if alarm.periodic.enable:
				# Check alarm has not been trigered yet
				if alarm.status == 'idle':
					# Check current weekday is enabled in alarm
					if alarm.periodic.weekday[wd]:
						# Check current time is alarm time
						if alarm.hour == hh and alarm.minute == mm:
							# Trigger alarm
							alarm.status = 'on'
							self.play(alarm)
				# Check if alarm is ON
				elif alarm.status == 'on' or alarm.status == 'snooze_on':
					# Check if volume ramp still applies
					if current_timestamp <= alarm.volume.tstop:
						# Check if user has manually modified volume
						if self.sound.volume != alarm.volume.current:
							if alarm.volume.current != -1:
								alarm.volume.current = -1
								print('Volume ramp-up cancelled due to user interaction')
						else:
							newvol=int(alarm.volume.start + (alarm.volume.end - alarm.volume.start)/(alarm.volume.tstop - alarm.volume.tstart) * (current_timestamp - alarm.volume.tstart))
							if newvol != alarm.volume.current:
								print('[alarm] Ramping up volume: ' + str(newvol))
								alarm.volume.current = newvol
								self.sound.set_volume(newvol)
					# Check if weather forecsat is enabled and not executed
					if alarm.weather.enable == True and alarm.weather.executed == False:
						if current_timestamp >= alarm.weather.timestamp:
							self.sound.say_text(alarm.weather.greeting + 
								'El tiempo ahora es ' +
								self.clock.forecast_currently() + 
								', con pronóstico ' +
								self.clock.forecast_hourly(), lang='es')
							alarm.weather.executed = True
					
				# Check if alarm is in snooze
				elif alarm.status == 'snooze_wait':
					# Check current time is snooze time
					if alarm.snooze.timestamp <= current_timestamp:
						# Trigger alarm
						print('[alarm] Alarm ' + alarm.name + ' going to snooze on mode')
						alarm.status = 'snooze_on'
						self.play(alarm)
				# Check if alarm is in off
				elif alarm.status == 'off':
					# Check current time is alarm time
					if alarm.hour == hh and alarm.minute == mm:
						# Wait until current time has changed
						pass
					else:
						# Go to idle again
						print('[alarm] Alarm ' + alarm.name + ' going to idle')
						alarm.status = 'idle'
					