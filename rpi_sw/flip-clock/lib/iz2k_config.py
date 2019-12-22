import os
from lxml import etree

class configuration:

	current_radio_station = 0
	
	def __init__(self):
	
		bindir = os.path.dirname(os.path.realpath(__file__))
		
		tree = etree.parse(bindir + '/../config/radio_stations.xml')
		self.radio_stations_freq = tree.getroot().xpath('//station/freq/text()')
		self.radio_stations_name = tree.getroot().xpath('//station/name/text()')


	def get_current_radio_freq(self):
		return self.radio_stations_freq[current_radio_station]
				
	def get_current_radio_freq(self):
		return self.radio_stations_freq[current_radio_station]
		