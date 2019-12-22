import time
from rpi_ws281x import Color, PixelStrip, ws

def color_off():
	return Color(0, 0, 0, 0)
	
class neoled:

	# LED strip configuration:
	LED_COUNT = 16         # Number of LED pixels.
	LED_PIN = 10           # GPIO pin connected to the pixels (must support PWM!).
	LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
	LED_DMA = 10           # DMA channel to use for generating signal (try 10)
	LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
	LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
	LED_CHANNEL = 0
	LED_STRIP = ws.SK6812_STRIP_GRBW
	
	def __init__(self):
		# Create NeoPixel object with appropriate configuration.
		self.strip = PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ,
						self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, 
						self.LED_CHANNEL, self.LED_STRIP)
		# Intialize the library (must be called once before other functions).
		self.strip.begin()
		self.colorFill(Color(0,0,0,0))

	# Define functions which animate LEDs in various ways.	
	def colorFill(self, color):
		"""Fill strip with color at once."""
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, color)
		self.strip.show()
		
	def colorWipe(self, color, wait_ms=10):
		"""Wipe color across display a pixel at a time."""
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, color)
			self.strip.show()
			time.sleep(wait_ms / 1000.0)
	
	def colorBlink(self, color, blink_ms=20, nblinks=1):
		for i in range(nblinks):
			self.colorFill(color)
			time.sleep(blink_ms / 1000.0)
			self.colorFill(Color(0,0,0,0))
			if i < (nblinks-1):
				time.sleep(blink_ms / 1000.0)
	
	def multColor(self, color, multiplier):
		white = (color >> 24) & 0xFF
		red = (color >> 16) & 0xFF
		green = (color >> 8) & 0xFF
		blue = color & 0xFF
		return Color(int(red*multiplier), int(green*multiplier), int(blue*multiplier), int(white*multiplier))
	
	def dualbulb(self, color, pos):
		dualbulb_pattern = {
				0:0.1,
				1:0.2,
				2:0.5,
				3:1,
				4:0.5,
				5:0.2,
				6:0.5,
				7:1,
				8:0.5,
				9:0.2,
				10:0.1,
				11:0.2,
				12:0.5,
				13:1,
				14:0.5,
				15:0.2,
			}
		return self.multColor(color, dualbulb_pattern[pos%16])
		
	def nightlight(self, color):
		wait_ms=25
		# Ramp UP 0-0.5
		s=0
		for j in range(10):
			s += 0.05
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, self.multColor(self.dualbulb(color, i), s))
			self.strip.show()
			time.sleep(wait_ms / 1000.0)
		for c in range(5):
			# Ramp UP 0.5-1
			s=0.5
			for j in range(10):
				s += 0.05
				for i in range(self.strip.numPixels()):
					self.strip.setPixelColor(i, self.multColor(self.dualbulb(color, i+c), s))
				self.strip.show()
				time.sleep(wait_ms / 1000.0)
			# Ramp DOWN 1-05
			for j in range(10):
				s -= 0.05
				for i in range(self.strip.numPixels()):
					self.strip.setPixelColor(i, self.multColor(self.dualbulb(color, i+c), s))
				self.strip.show()
				time.sleep(wait_ms / 1000.0)
		# Ramp DOWN 0.5-0
		for j in range(10):
			s -= 0.05
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, self.multColor(self.dualbulb(color, i), s))
			self.strip.show()
			time.sleep(wait_ms / 1000.0)
		self.colorFill(Color(0,0,0))

	def wheel(self, pos):
		"""Generate rainbow colors across 0-255 positions."""
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)

	def rainbow(self, wait_ms=20, iterations=1):
		"""Draw rainbow that fades across all pixels at once."""
		for j in range(256 * iterations):
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, wheel((i + j) & 255))
			self.strip.show()
			time.sleep(wait_ms / 1000.0)

	def rainbowCycle(self, wait_ms=20, iterations=5):
		"""Draw rainbow that uniformly distributes itself across all pixels."""
		for j in range(256 * iterations):
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, wheel(((i * 256 // self.strip.numPixels()) + j) & 255))
			self.strip.show()
			time.sleep(wait_ms / 1000.0)
		