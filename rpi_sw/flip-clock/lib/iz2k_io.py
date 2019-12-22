# pushbutton class based on pigpio library
# version: 0.0.1

import pigpio
import time


class fake_tie:

	# Default values for the switch
	pin = None

	def __init__(self, pin=None, tie=None):
		if (pin is not None) and (tie is not None):
			self.pin = pin
			self.pin_ctrl = pigpio.pi()
			self.pin_ctrl.write(pin, tie)



class switch:

	# Default values for the switch
	sw_debounce = 300
	long_press_opt = False
	sw_short_callback = None
	sw_long_callback = None
	wait_time = time.time()
	long = False

	def __init__(self, I=None, G=None):
			
		def sw_rise(gpio, level, tick):
			if self.long_press_opt:
				if not self.long:
					self.short_press()

		def sw_fall(gpio, level, tick):
			if self.long_press_opt:
				self.long = False
				press_time = time.time()
				while self.pi.read(self.I) == 0:
					self.wait_time = time.time()
					time.sleep(0.1)
					if self.wait_time - press_time > 1:
						self.long_press()
						self.long = True
						break
			else:
				self.short_press()

		if I is not None:
			self.I = I
			self.pi = pigpio.pi()
			self.pi.set_mode(I, pigpio.INPUT)
			self.pi.set_pull_up_down(self.I, pigpio.PUD_UP)
			self.pi.set_glitch_filter(self.I, self.sw_debounce)
			self.sw_falling = self.pi.callback(self.I, pigpio.FALLING_EDGE, sw_fall)
			self.sw_rising = self.pi.callback(self.I, pigpio.RISING_EDGE, sw_rise)

		# Set fake ground if specified
		if G is not None:
			self.pi.set_mode(G, pigpio.OUTPUT)
			self.pi.write(G, 0)
			


	def setup_switch(self, **kwargs):
		if 'debounce' in kwargs:
			self.sw_debounce = kwargs['debounce']
		if 'long_press' in kwargs:
			self.long_press_opt = kwargs['long_press']
		if 'sw_short_callback' in kwargs:
			self.sw_short_callback = kwargs['sw_short_callback']
		if 'sw_long_callback' in kwargs:
			self.sw_long_callback = kwargs['sw_long_callback']

	def short_press(self):
		self.sw_short_callback()

	def long_press(self):
		self.sw_long_callback()


class rotary:

	last_A = 1
	last_B = 1
	last_gpio = 0
	
	last_event_time = time.time()
	debounce_time = 0

	def __init__(self, A=None, B=None, G=None, callback=None):
		if not A or not B:
			raise BaseException("Encoder pins must be specified!")
		self.pi = pigpio.pi()
		self.Enc_A = A
		self.Enc_B = B
		self.callback = callback
		
		self.pi.set_mode(self.Enc_A, pigpio.INPUT)
		self.pi.set_pull_up_down(self.Enc_A, pigpio.PUD_UP)
		self.pi.set_mode(self.Enc_B, pigpio.INPUT)
		self.pi.set_pull_up_down(self.Enc_B, pigpio.PUD_UP)
		
		# Set fake ground if specified
		if G is not None:
			self.pi.set_mode(G, pigpio.OUTPUT)
			self.pi.write(G, 0)
		
		def rotary_interrupt(gpio,level,tim):
			if gpio == self.Enc_A:
				self.last_A = level
			else:
				self.last_B = level;
				
			if gpio != self.last_gpio:
				self.last_gpio = gpio
				if gpio == self.Enc_A and level == 1:
					if self.last_B == 1:
						if time.time() - self.last_event_time > self.debounce_time:
							self.last_event_time = time.time()
							if self.callback is not None:
								self.callback(-1)
				elif gpio == self.Enc_B and level == 1:
					if self.last_A == 1:
						if time.time() - self.last_event_time > self.debounce_time:
							self.last_event_time = time.time()
							if self.callback is not None:
								self.callback(1)
		
		self.pi.callback(self.Enc_A, pigpio.EITHER_EDGE, rotary_interrupt)
		self.pi.callback(self.Enc_B, pigpio.EITHER_EDGE, rotary_interrupt)
		
		
		