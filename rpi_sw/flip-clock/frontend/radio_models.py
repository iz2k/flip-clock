# forms.py

from wtforms import Form, StringField, IntegerField, SelectField, DecimalField, SubmitField, HiddenField, validators
from decimal import Decimal
from lxml import etree


class RadioStation:
	freq = 0
	name = ''

	def __init__(self, form=None, xml=None):
		if form != None:
			self.parseForm(form)
		if xml != None:
			self.parseXML(xml)

	def parseForm(self, form):
		self.name = form.name.data
		self.freq = form.freq.data

	def parseXML(self, xml):
		for ch in xml.getchildren():
			if ch.tag == 'freq':
				self.freq = Decimal(ch.text)
			if ch.tag == 'name':
				self.name = ch.text

class RadioStationForm(Form):
	idx = HiddenField()
	freq = DecimalField('Frequency:', places=2, render_kw={"placeholder": "MHz", "style":"font-size:20px", "size":"2"})
	name = StringField('Name', render_kw={"placeholder": "Radio Station Name", "style":"font-size:20px", "size":"17"})
	delete = SubmitField(label='Delete')
	update = SubmitField(label='Update')
	new = SubmitField(label='New')
	up = SubmitField(label='Up')
	down = SubmitField(label='Down')
	pos = IntegerField('Position:', render_kw={"size":"1"})
	setpos = SubmitField(label='Set')
	lastfreq = HiddenField('Last tuned frequency')

	def readobject(self, rstation):
		self.freq.data = rstation.freq
		self.name.data = rstation.name

class RadioControlForm(Form):
	freq = DecimalField('Frequency:', places=2)
	tune = SubmitField(label='Tune')
	dec = SubmitField(label='<<')
	inc = SubmitField(label='>>')
	swoff = SubmitField(label='Switch off')

def save_radio_list(rstations, filename):
	# Create main element
	rlist = etree.Element('radio_stations')
	for rstation in rstations:
		# Create station element
		rs = etree.SubElement(rlist, 'station')
		# Main tags
		se = etree.SubElement(rs, 'freq')
		se.text = str(rstation.freq)
		se = etree.SubElement(rs, 'name')
		se.text = str(rstation.name)

	with open(filename, 'w', encoding='utf8') as doc:
		doc.write(etree.tostring(rlist, pretty_print=True, encoding='unicode'))

def load_radio_list(filename):
    tree = etree.parse(filename)

    # Create radio_station objects from XML
    rstations = []
    for el in tree.findall('station'):
        rstation = RadioStation(xml=el)
        rstations.append(rstation)

    # Return radio_station object list
    return rstations