import shlex
import subprocess
from app import app
from alarm_models import Alarm, AlarmForm, save_alarm_list
from flask import flash, render_template, request, redirect
import decimal
from lxml import etree

@app.route('/alarm', methods=['GET', 'POST'])
def alarm_index():
	tree = etree.parse('alarms.xml')

	# Create alarm objects from XML
	alarms=[]
	for el in tree.findall('alarm'):
		alarm = Alarm(xml=el)
		alarms.append(alarm)

	if request.method == 'POST':
		reqform = AlarmForm(request.form)
		if reqform.new.data:
			print('Adding new alarm')
			alarm = Alarm(form=reqform)
			alarms.append(alarm)
		if reqform.update.data:
			print('Updating alarm')
			alarms[int(reqform.idx.data)].parseForm(reqform)
		if reqform.delete.data:
			print('Deleting alarm')
			alarms.pop(int(reqform.idx.data))
		save_alarm_list(alarms=alarms, filename='alarms.xml')

	# Create alarm forms from objects
	alarmforms=[]
	for idx, el in enumerate(alarms):
		alarmform = AlarmForm()
		alarmform.readobject(el)
		alarmform.idx.data=idx
		alarmforms.append(alarmform)

	return render_template('alarm.html', aforms=alarmforms, nalarms=len(alarmforms), aformnew=AlarmForm())

