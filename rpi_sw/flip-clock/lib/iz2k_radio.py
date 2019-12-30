import os
import subprocess
import shlex
import time
from lxml import etree


class radio:

	current_radio_station = 0
	
	def __init__(self):
	
		bindir = os.path.dirname(os.path.realpath(__file__))
		
		tree = etree.parse(bindir + '/../config/radio_stations.xml')
		self.radio_stations_freq = tree.getroot().xpath('//station/freq/text()')
		self.radio_stations_name = tree.getroot().xpath('//station/name/text()')

	def kill_radio(self):
		print("[radio] Radio OFF")

		# Kill previous instances
		subprocess.call(['pkill', '-9', 'softfm'])
		
	def play_radio(self):
		print("[radio] Tunning radio: [" + self.radio_stations_freq[self.current_radio_station] + "MHz] " 
				+ self.radio_stations_name[self.current_radio_station])
	
		# Kill previous instances
		subprocess.call(['pkill', '-9', 'softfm'])
		subprocess.call(['pkill', '-9', 'mplayer'])
		
		# Speak out radio name
		cmd = shlex.split('mplayer -ao alsa -af volume=10 -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=' 
					+ self.radio_stations_name[self.current_radio_station] + '&tl=es"')
		subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		
		# Synthonize radio
		cmd=shlex.split('softfm -f ' + self.radio_stations_freq[self.current_radio_station] + 'M')
		subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	def next_station(self):
		self.current_radio_station += 1
		if (self.current_radio_station >= len(self.radio_stations_freq)):
				self.current_radio_station=0
		self.play_radio()
		
	def previous_station(self):
		self.current_radio_station -= 1
		if (self.current_radio_station < 0):
				self.current_radio_station=len(self.radio_stations_freq)-1
		self.play_radio()
		
