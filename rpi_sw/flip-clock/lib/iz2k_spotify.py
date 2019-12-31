import os
import subprocess
import shlex
import time
from lxml import etree
from frontend import spotify_models


class spotify:

	current_playlist = 0
	tizonia = None
	spotitems=[]
	spotlists=[]
	
	def __init__(self):
	
		bindir = os.path.dirname(os.path.realpath(__file__))
		self.spotitems = spotify_models.load_spotitem_list(bindir + '/../config/spotify.xml')
		
		for spotitem in self.spotitems:
			if spotitem.type == 'Playlist':
				self.spotlists.append(spotitem)

	def kill_spotify(self):
		print("[spotify] Spotify OFF")

		if self.tizonia is not None:
			self.tizonia.terminate()
			self.tizonia = None
		# Kill previous instances
		subprocess.call(['pkill', '-9', 'softfm'])
	
	def play_spotify(self):
		self.play_list(self.spotlists[self.current_playlist])
	
	def play_track(self, URI):
		# Terminate previous instance if running
		if self.tizonia is not None:
			self.kill_spotify()
		
		print("[spotify] Playing track: " + URI)
		# Play track
		cmd=shlex.split('tizonia --spotify-track-id ' + URI)
		subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

	def play_list(self, pl):
		# Terminate previous instance if running
		if self.tizonia is not None:
			self.kill_spotify()
		
		print("[spotify] Playing playlist: " + pl.name + '(' + pl.URI + ')')
		
		# Speak out radio name
		#subprocess.call(['pkill', '-9', 'mplayer'])
		cmd = shlex.split('mplayer -ao alsa -af volume=10 -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=' 
					+ pl.name + '&tl=es"')
		subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		

		# Play playlist
		raw_cmd = 'tizonia --spotify-playlist-id ' + pl.URI
		if pl.shuffle:
			raw_cmd += ' -s'
		cmd=shlex.split(raw_cmd)
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
		self.current_playlist += 1
		if (self.current_playlist >= len(self.spotlists)):
				self.current_playlist=0
		self.play_spotify()
		
	def previous_list(self):
		self.current_playlist -= 1
		if (self.current_playlist < 0):
				self.current_playlist=len(self.spotlists)-1
		self.play_spotify()
		
