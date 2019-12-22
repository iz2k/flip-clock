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
		#color=rgbw2color(rgbw)
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, color)
		self.strip.show()
		
	def colorWipe(self, color, wait_ms=10):
		#color=rgbw2color(rgbw)
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
		