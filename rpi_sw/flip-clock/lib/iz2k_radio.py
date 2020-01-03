import os
import subprocess
import shlex
import time
from lxml import etree
from frontend import radio_models


class radio:

	def __init__(self, sound):
		self.reload_xml()
		self.current_radio_station = 0
		self.softfm=None
		self.sound=sound

	def reload_xml(self):
		print('[radio] Loading radio station list')
		# Load radio stations from XML
		bindir = os.path.dirname(os.path.realpath(__file__))
		self.radio_stations= radio_models.load_radio_list(bindir + '/../config/radio_stations.xml')	
	
	def kill_radio(self):
		if self.softfm is not None:
			print("[radio] Radio OFF")
			self.softfm.terminate()
			self.softfm.wait()

	def tune_freq(self, freq):
		cmd=shlex.split('softfm -f ' + str(freq) + 'M')
		self.softfm = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		

	def play_radio(self):
		# Kill previous instances
		self.kill_radio()
		
		print("[radio] Tunning radio: [" + str(self.radio_stations[self.current_radio_station].freq) + "MHz] " 
				+ self.radio_stations[self.current_radio_station].name)

		# Speak out radio name
		self.sound.say_text(self.radio_stations[self.current_radio_station].name, lang='es')

		# Synthonize radio
		self.tune_freq(self.radio_stations[self.current_radio_station].freq)

	def next_station(self):
		print('[radio] Moving to next station...')
		self.current_radio_station += 1
		if (self.current_radio_station >= len(self.radio_stations)):
				self.current_radio_station=0
		self.play_radio()

	def previous_station(self):
		print('[radio] Moving to previous station...')
		self.current_radio_station -= 1
		if (self.current_radio_station < 0):
				self.current_radio_station=len(self.radio_stations)-1
		self.play_radio()
