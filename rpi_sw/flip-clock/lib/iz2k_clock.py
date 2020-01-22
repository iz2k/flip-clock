import time
from serial import Serial
from datetime import datetime
from darksky.api import DarkSky, DarkSkyAsync
from darksky.types import languages, units, weather
from frontend.app import clockcalibration
	
class clock:
	
	UART_PORT = '/dev/ttyS0'
	UART_BR = 115200
	
	WEATHER_UPDATE_RATE = 600 # 600 seconds = 10 minutes
	
	last_mm = 0
	last_ss = 0
	next_ww = WEATHER_UPDATE_RATE
	
	def __init__(self, darksky):
		self.comport = Serial('/dev/ttyS0', baudrate=115200)
		self.forecast = None
		self.calibrating=False
		self.darksky_secret = darksky
		clockcalibration.put(False)

	def set_secret(self, darksky):
		print('[clock] DarkSky secret set.')
		self.darksky_secret = darksky

	def calibration(self, status):
		if status==True and self.calibrating==False:
			print('[clock] Calibration enabled')
			self.calibrating=True
		elif status==False and self.calibrating==True:
			print('[clock] Calibration disabled')
			self.calibrating=False
			cmd = 'r'
			cmd += '\r'
			print("[clock] Run command: ", cmd)
			self.comport.write(bytes(cmd, 'UTF-8'))
		
		clockcalibration.put(self.calibrating)

	def set(self, msg):
		print(msg)
		if 'clock-set-HH-' in msg:
			cmd = msg.replace('clock-set-HH-', 'h')
		elif 'clock-set-MM-' in msg:
			cmd = msg.replace('clock-set-MM-', 'm')
		elif 'clock-set-WW-' in msg:
			cmd = msg.replace('clock-set-WW-', 'w')
		
		cmd += '\r'
		print("[clock] Set command: ", cmd)
		self.comport.write(bytes(cmd, 'UTF-8'))
		
	
	def sync(self, msg):
		print(msg)
		if 'clock-sync-HH' in msg:
			cmd = 'sh'
		elif 'clock-sync-MM' in msg:
			cmd = 'sm'
		elif 'clock-sync-WW' in msg:
			cmd = 'sw'
		
		cmd += '\r'
		print("[clock] Sync command: ", cmd)
		self.comport.write(bytes(cmd, 'UTF-8'))
		
	def cal(self, msg):
		print(msg)
		if 'clock-cal-HH' in msg:
			cmd = msg.replace('clock-cal-HH-', 'ch')
		elif 'clock-cal-MM' in msg:
			cmd = msg.replace('clock-cal-MM-', 'cm')
		elif 'clock-cal-WW' in msg:
			cmd = msg.replace('clock-cal-WW-', 'cw')
		
		cmd += '\r'
		print("[clock] Cal command: ", cmd)
		self.comport.write(bytes(cmd, 'UTF-8'))
	def update_time(self):
		command =  'T' + str(self.now.hour).zfill(2) + str(self.now.minute).zfill(2) + '\r'
		print("Updating time: ", command)
		self.comport.write(bytes(command, 'UTF-8'))
			
	def update_weather(self):
		# Get weather
		print("Updating weather:")
		darksky = DarkSky(self.darksky_secret)
		try:
			self.forecast = darksky.get_forecast(43.312691, -1.993332, lang='es')

			print(" >> Summary: ", self.forecast.currently.summary)
			print(" >> Icon: ", self.forecast.currently.icon)
			print(" >> Temperature: ", self.forecast.currently.temperature)
			print(" >> Humidity: ", self.forecast.currently.humidity)
			print(" >> Wind Speed: ", self.forecast.currently.wind_speed)
			print(" >> Pressure: ", self.forecast.currently.pressure)

			print(' >> Current summary: ' + self.forecast.currently.summary)
			#print(' >> Minutely summary: ' + self.forecast.minutely.summary)
			print(' >> Hourly summary: ' + self.forecast.hourly.summary)

			print("Get icon index:")
			weather_icons = {
				"clear-day":"01",
				"clear-night":"02",
				"partly-cloudy-day":"03",
				"partly-cloudy-night":"04",
				"cloudy":"05",
				"fog":"06",
				"wind":"07",
				"sleet":"08",
				"rain":"09",
				"snow":"10",
			}
			weather_icon_index=weather_icons.get(self.forecast.currently.icon)
			print(" >> Icon index: ", weather_icon_index)
			
			command =  'W' + weather_icon_index + '\r'
			print("Weather command: ", command)
			self.comport.write(bytes(command, 'UTF-8'))
		except:
			print("Exception occured during weather update")
	
	def forecast_currently(self):
		if self.forecast is not None:
			return self.forecast.currently.summary
		else:
			return 'No hay datos disponibles.'
			
	def forecast_minutely(self):
		if self.forecast is not None:
			return self.forecast.minutely.summary
		else:
			return 'No hay datos disponibles.'
			
	def forecast_hourly(self):
		if self.forecast is not None:
			return self.forecast.hourly.summary
		else:
			return 'No hay datos disponibles.'
	
	def run(self):
		if(self.calibrating==False):
			self.now = datetime.now()
			if(self.now.minute != self.last_mm):
				self.last_mm = self.now.minute
				self.update_time()
				
			if self.next_ww == self.WEATHER_UPDATE_RATE:
				self.next_ww = 0
				self.update_weather()
			else:
				if self.now.second != self.last_ss:
					self.last_ss = self.now.second
					self.next_ww += 1
		
		