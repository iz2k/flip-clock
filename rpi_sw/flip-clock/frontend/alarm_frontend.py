from .app import app, frontendqueue
from .alarm_models import Alarm, AlarmForm, save_alarm_list, load_alarm_list
from flask import render_template, request
import os

@app.route('/alarm', methods=['GET', 'POST'])
def alarm_index():
	# Load stored alarm objects
	rundir = os.path.dirname(os.path.realpath(__file__))
	alarms = load_alarm_list(rundir + '/../config/alarms.xml')

	if request.method == 'POST':
		reqform = AlarmForm(request.form)
		if reqform.new.data:
			print('[frontend][alarm] Adding new alarm')
			alarm = Alarm(form=reqform)
			alarms.append(alarm)
		if reqform.update.data:
			print('[frontend][alarm] Updating alarm')
			alarms[int(reqform.idx.data)].parseForm(reqform)
		if reqform.delete.data:
			print('[frontend][alarm] Deleting alarm')
			alarms.pop(int(reqform.idx.data))
		save_alarm_list(alarms=alarms, filename=rundir + '/../config/alarms.xml')
		frontendqueue.put('alarm_update')

	# Create alarm forms from objects
	alarmforms=[]
	for idx, el in enumerate(alarms):
		alarmform = AlarmForm()
		alarmform.readobject(el)
		alarmform.idx.data=idx
		alarmforms.append(alarmform)

	return render_template('alarm.html', aforms=alarmforms, nalarms=len(alarmforms), aformnew=AlarmForm())

