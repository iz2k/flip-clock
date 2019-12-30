import os
import subprocess
import shlex
import time
from lxml import etree


class spotify:

	current_playlist = 0
	tizonia = None
	
	def __init__(self):
	
		bindir = os.path.dirname(os.path.realpath(__file__))
		
		#tree = etree.parse(bindir + '/../config/radio_stations.xml')
		#self.radio_stations_freq = tree.getroot().xpath('//station/freq/text()')
		#self.radio_stations_name = tree.getroot().xpath('//station/name/text()')

	def kill_spotify(self):
		print("[spotify] Spotify OFF")

		if self.tizonia is not None:
			self.tizonia.terminate()
			self.tizonia = None
		# Kill previous instances
		subprocess.call(['pkill', '-9', 'softfm'])
		
	def play_track(self, URI):
		print("[spotify] Playing track: " + URI)
	
		# Terminate previous instance if running
		if self.tizonia is not None:
			self.kill_spotify()
			
		# Play track
		cmd=shlex.split('tizonia --spotify-track-id ' + URI)
		subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	def play_list(self, URI):
		print("[spotify] Playing playlist: " + URI)
	
		# Terminate previous instance if running
		if self.tizonia is not None:
			self.kill_spotify()
			
		# Play playlist
		cmd=shlex.split('tizonia --spotify-playlist-id ' + URI)
		self.tizonia = subprocess.Popen(cmd,stdin=subprocess.PIPE, 
										stdout=subprocess.DEVNULL, 
										stderr=subprocess.STDOUT, 
										bufsize=1, 
										universal_newlines=True)

	def next_track(self):
		if self.tizonia is not None:
			self.tizonia.stdin.write('n\n')
		
	def previous_track(self):	
		if self.tizonia is not None:
			self.tizonia.stdin.write('p\n')
		
	def next_list(self):
		self.current_radio_station += 1
		if (self.current_radio_station >= len(self.radio_stations_freq)):
				self.current_radio_station=0
		self.play_radio()
		
	def previous_list(self):
		self.current_radio_station -= 1
		if (self.current_radio_station < 0):
				self.current_radio_station=len(self.radio_stations_freq)-1
		self.play_radio()
		
