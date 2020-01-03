import os
import subprocess
import shlex
import time
from lxml import etree
from frontend import spotify_models


class spotify:

	def __init__(self, sound):
		self.reload_xml()
		self.current_item = 0
		self.tizonia = None
		self.sound=sound

	def reload_xml(self):
		print('[spotify] Loading spotitem list')
		# Load spotitems from XML
		bindir = os.path.dirname(os.path.realpath(__file__))
		self.spotitems = spotify_models.load_spotitem_list(bindir + '/../config/spotify.xml')

	def kill_spotify(self):
		if self.tizonia is not None:
			print("[spotify] Spotify OFF")
			self.tizonia.terminate()
			self.tizonia.wait()

	def play_spotify(self):
		print('[spotify] Launching item: ' + self.spotitems[self.current_item].name)

		# Speak out item name
		self.sound.say_text(self.spotitems[self.current_item].name, lang='es')

		# Play item
		self.play_URI(self.spotitems[self.current_item].URI, self.spotitems[self.current_item].shuffle)

	def play_URI(self, URI, shuffle):
		if 'playlist' in URI:
			self.play_list(URI=URI, shuffle=shuffle)
		else:
			self.play_track(URI=URI)

	def play_track(self, URI):
		# Terminate previous instance if running
		if self.tizonia is not None:
			self.kill_spotify()

		print("[spotify] Playing track: " + URI)
		# Play track
		cmd=shlex.split('tizonia --spotify-track-id ' + URI)
		subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	def play_list(self, URI, shuffle=False):
		# Terminate previous instance if running
		if self.tizonia is not None:
			self.kill_spotify()

		print("[spotify] Playing playlist: " + URI)
		# Play playlist
		raw_cmd = 'tizonia --spotify-playlist-id ' + URI
		if shuffle:
			raw_cmd += ' -s'
		cmd=shlex.split(raw_cmd)
		self.tizonia = subprocess.Popen(cmd,stdin=subprocess.PIPE, 
						stdout=subprocess.DEVNULL, 
						stderr=subprocess.STDOUT, 
						bufsize=1, 
						universal_newlines=True)

	def next_track(self):
		if self.tizonia is not None:
			print("[spotify] Next track")
			self.tizonia.stdin.write('n\n')

	def previous_track(self):	
		if self.tizonia is not None:
			print("[spotify] Previous track")
			self.tizonia.stdin.write('p\n')

	def next_list(self):
		print("[spotify] Next spotitem")
		self.current_item += 1
		if (self.current_item >= len(self.spotitems)):
				self.current_item=0
		self.play_spotify()

	def previous_list(self):
		print("[spotify] Previous spotitem")
		self.current_item -= 1
		if (self.current_item < 0):
				self.current_item=len(self.spotitems)-1
		self.play_spotify()
