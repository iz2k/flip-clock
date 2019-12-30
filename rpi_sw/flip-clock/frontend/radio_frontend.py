import shlex
import subprocess
from app import app
from radio_models import RadioControlForm, RadioStationForm, RadioStation, save_radio_list
from flask import flash, render_template, request, redirect
from decimal import Decimal
from lxml import etree

@app.route('/radio', methods=['GET', 'POST'])
def radio_index():
	lastfreq=Decimal(88.0)

	tree = etree.parse('radio_stations.xml')
	# Create alarm objects from XML
	rstations=[]
	for el in tree.findall('station'):
		station = RadioStation(xml=el)
		rstations.append(station)

	if request.method == 'POST':
		reqform = RadioStationForm(request.form)
		idx=int(reqform.idx.data)
		if reqform.new.data:
			print('Adding new station')
			rstation = RadioStation(form=reqform)
			rstations.append(rstation)
		elif reqform.update.data:
			print('Updating station')
			rstations[idx].parseForm(reqform)
		elif reqform.delete.data:
			print('Deleting station')
			rstations.pop(idx)
		elif reqform.up.data:
			if idx > 0:
				print('Moving up station')
				rstations.insert(idx-1, rstations.pop(idx))
		elif reqform.down.data:
			if idx<len(rstations)-1:
				print('Moving down station')
				rstations.insert(idx+1, rstations.pop(idx))
		elif reqform.setpos.data:
			if reqform.pos.data < len(rstations) + 1 and reqform.pos.data > 0:
				print('Moving station to position')
				rstations.insert(reqform.pos.data-1, rstations.pop(idx))
		save_radio_list(rstations=rstations, filename='radio_stations.xml')
		lastfreq=Decimal(reqform.lastfreq.data)

	# Create radio station forms from objects
	radioforms=[]
	for idx, el in enumerate(rstations):
		radioform = RadioStationForm()
		radioform.readobject(el)
		radioform.idx.data=idx
		radioform.pos.data=idx+1
		radioform.lastfreq.data=lastfreq
		radioforms.append(radioform)

	ctrlform = RadioControlForm(None)
	ctrlform.freq.data = lastfreq

	return render_template('radio.html', cform=ctrlform, sform=radioforms, nstations=len(radioforms), sformnew=RadioStationForm(None))

@app.route('/tuneradio', methods=['GET', 'POST'])
def tune_radio():
	radiocontrol = RadioControlForm(request.form)

	if request.method == 'POST':
		# Kill previous instances
		#subprocess.call(['pkill', '-9', 'softfm'])
		#subprocess.call(['pkill', '-9', 'mplayer'])
		if radiocontrol.swoff.data:
			print('Switching radio OFF')
		else:
			if radiocontrol.tune.data:
				pass
			if radiocontrol.dec.data:
				radiocontrol.freq.data -= Decimal(0.1)
			if radiocontrol.inc.data:
				radiocontrol.freq.data += Decimal(0.1)

			radiocontrol.freq.data = round(radiocontrol.freq.data, 2)
			radiocontrol.freq.raw_data = [str(radiocontrol.freq.data)]

			# Synthonize radio
			print('Tunning', radiocontrol.freq.data, 'MHz')
			cmd = shlex.split('softfm -f ' + str(radiocontrol.freq.data) + 'M')
			#subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	else:
		radiocontrol.freq.data = Decimal(88)

	return render_template('tuneradio.html', cform=radiocontrol)