from frontend import alarm_models
import os
from datetime import datetime

class alarmclock:

	def __init__(self, sound, spotify, radio, strip, clock):
		self.sound = sound
		self.spotify = spotify
		self.radio = radio
		self.strip = strip
		self.clock = clock
		
		# Load alarms from XML
		bindir = os.path.dirname(os.path.realpath(__file__))
		self.alarms = alarm_models.load_alarm_list(bindir + '/../config/alarms.xml')


	def snooze(self):
		pass
		
	def run(self):
		now = datetime.now()
		hh = now.hour
		mm = now.minute
		wd = now.weekday()
		# Go through all alarms
		for alarm in self.alarms:
			# Check current weekday is enabled in alarm
			if alarm.periodic.weekday[wd]:
				# Check current time is alarm time
				if alarm.hour == hh and alarm.minute == mm:
					# Check alarm has not been trigered yet
					if alarm.status == 'idle':
						# Trigger alarm
						alarm.status = 'on'
						# Determine source
						if alarm.source.type=='spotify':
							print('triggering spotify alarm')
							# Kill previous playbacks if exist
							self.radio.kill_radio()
							self.spotify.kill_spotify()
							self.spotify.play_URI(URI=alarm.source.item, shuffle=alarm.source.randomize)
						elif alarm.source.type=='radio':
							print('triggering radio alarm')
							# Kill previous playbacks if exist
							self.radio.kill_radio()
							self.spotify.kill_spotify()
					