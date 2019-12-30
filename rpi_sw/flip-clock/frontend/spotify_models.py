from wtforms import Form, StringField, BooleanField, SelectField, DecimalField, SubmitField, HiddenField
from tools import str2bool
from lxml import etree


class Spotitem:
	name = None
	type = None
	URI = None
	shuffle = None

	def __init__(self, form=None, xml=None):
		if form != None:
			self.parseForm(form)
		if xml != None:
			self.parseXML(xml)

	def parseForm(self, form):
		self.name = form.name.data
		self.type = form.type.data
		self.URI = form.URI.data
		self.shuffle = form.shuffle.data

	def parseXML(self, xml):
		for ch in xml.getchildren():
			if ch.tag == 'name':
				self.name = ch.text
			if ch.tag == 'type':
				self.type = ch.text
			if ch.tag == 'URI':
				self.URI = ch.text
			if ch.tag == 'shuffle':
				self.shuffle = str2bool(ch.text)

class SpotitemForm(Form):
	idx = HiddenField()
	name = StringField('Name')
	type_choices = [('Track', 'Track'),
			   ('Playlist', 'Playlist')]
	type = SelectField('Type', choices=type_choices)
	URI = StringField('URI')
	shuffle = BooleanField('shuffle')
	delete = SubmitField(label='Delete')
	update = SubmitField(label='Update')
	new = SubmitField(label='New')

	def readobject(self, spotitem):
		self.name.data = spotitem.name
		self.type.data = spotitem.type
		self.URI.data = spotitem.URI
		self.shuffle.data = spotitem.shuffle


def save_spotitem_list(spotitems, filename):
	# Create main element
	slist = etree.Element('spotitems')
	for sitem in spotitems:
		# Create station element
		rs = etree.SubElement(slist, 'spotitem')
		# Main tags
		se = etree.SubElement(rs, 'name')
		se.text = str(sitem.name)
		se = etree.SubElement(rs, 'type')
		se.text = str(sitem.type)
		se = etree.SubElement(rs, 'URI')
		se.text = str(sitem.URI)
		se = etree.SubElement(rs, 'shuffle')
		se.text = str(sitem.shuffle)

	with open(filename, 'w', encoding='utf8') as doc:
		doc.write(etree.tostring(slist, pretty_print=True, encoding='unicode'))

def load_spotitem_list(filename):
    tree = etree.parse(filename)

    # Create spotitem objects from XML
    spotitems = []
    for el in tree.findall('spotitem'):
        print(el)
        spotitem = Spotitem(xml=el)
        spotitems.append(spotitem)

    # Return spotitem object list
    return spotitems