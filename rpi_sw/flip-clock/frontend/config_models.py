from wtforms import Form, StringField, BooleanField, SelectField, DecimalField, SubmitField, HiddenField, PasswordField
from .tools import str2bool
from lxml import etree


class Config:

	def __init__(self, form=None, xml=None):
		self.darksky_secret = None
		self.spotify_user = None
		self.spotify_pass = None
		if form != None:
			self.parseForm(form)
		if xml != None:
			self.parseXML(xml)

	def parseForm(self, form):
		self.darksky_secret = form.darksky_secret.data
		self.spotify_user = form.spotify_user.data
		self.spotify_pass = form.spotify_pass.data

	def parseXML(self, xml):
		for ch in xml.getchildren():
			if ch.tag == 'darksky_secret':
				self.darksky_secret = ch.text
			if ch.tag == 'spotify_user':
				self.spotify_user = ch.text
			if ch.tag == 'spotify_pass':
				self.spotify_pass = ch.text

class ConfigForm(Form):
	darksky_secret = StringField('DarkSky secret', render_kw={"placeholder": "DarkSky secret", "size":"30"})
	spotify_user = StringField('Spotify Username', render_kw={"placeholder": "Spotify Username", "size":"15"})
	spotify_pass = PasswordField('Spotify Password', render_kw={"placeholder": "Spotify Password", "size":"15"})
	save = SubmitField(label='Save')

	def readobject(self, config):
		self.darksky_secret.data = config.darksky_secret
		self.spotify_user.data = config.spotify_user
		self.spotify_pass.data = config.spotify_pass


def save_config(config, filename):
	# Create main element
	et = etree.Element('config')
	# Create cfg element
	cfg = etree.SubElement(et, 'cfg')
	# Main tags
	se = etree.SubElement(cfg, 'darksky_secret')
	se.text = str(config.darksky_secret)
	se = etree.SubElement(cfg, 'spotify_user')
	se.text = str(config.spotify_user)
	se = etree.SubElement(cfg, 'spotify_pass')
	se.text = str(config.spotify_pass)

	with open(filename, 'w', encoding='utf8') as doc:
		doc.write(etree.tostring(et, pretty_print=True, encoding='unicode'))

def load_config(filename):
	tree = etree.parse(filename)
	
	# Create configuration object from XML
	el = tree.find('cfg')
	cfg = Config(xml=el)

	# Return configuration object
	return cfg