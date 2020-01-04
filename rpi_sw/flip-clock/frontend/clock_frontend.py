from .app import app, frontendqueue
from .clock_models import FClockForm
from flask import render_template, request
import os


@app.route('/clock', methods=['GET', 'POST'])
def clock_index():

	# Create clock form
	clockform = FClockForm()
	
	if request.method == 'POST':
		clockform = FClockForm(request.form)
		if clockform.set_hh.data:
			print('[frontend][clock] Setting HH')
		if clockform.set_mm.data:
			print('[frontend][clock] Setting MM')
			#spotitems[int(reqform.idx.data)].parseForm(reqform)
		frontendqueue.put('clock_control')

	print(clockform.calibrating)
	print(clockform.calibrating.data)

	return render_template('clock.html', cform=clockform)

