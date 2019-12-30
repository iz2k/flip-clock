from app import app
from alarm_models import Alarm, AlarmForm, save_alarm_list, load_alarm_list
from flask import render_template, request

@app.route('/alarm', methods=['GET', 'POST'])
def alarm_index():
	# Load stored alarm objects
	alarms = load_alarm_list('alarms.xml')

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

