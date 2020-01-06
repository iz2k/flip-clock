from .app import app, frontendqueue, clockcalibration
from .clock_models import FClockForm
from flask import render_template, request
import os


@app.route('/clock', methods=['GET', 'POST'])
def clock_index():

	# Create clock form
	clockform = FClockForm()
	# Read current clock status from queue	
	while clockcalibration.empty() is False:
		clockform.calibrating.data = clockcalibration.get()
	
	if request.method == 'POST':
		clockform = FClockForm(request.form)
		if clockform.set_hh.data:
			print('[frontend][clock] Setting HH')
			cmd='clock-set-HH-' + str(clockform.hh.data).zfill(2)
			frontendqueue.put(cmd)
		if clockform.set_mm.data:
			print('[frontend][clock] Setting MM')
			cmd='clock-set-MM-' + str(clockform.mm.data).zfill(2)
			frontendqueue.put(cmd)
		if clockform.set_ww.data:
			print('[frontend][clock] Setting WW')
			cmd='clock-set-WW-' + str(clockform.ww.data).zfill(2)
			frontendqueue.put(cmd)
		if clockform.sync_hh.data:
			print('[frontend][clock] Synching HH')
			cmd='clock-sync-HH'
			frontendqueue.put(cmd)
		if clockform.sync_mm.data:
			print('[frontend][clock] Synching MM')
			cmd='clock-sync-MM'
			frontendqueue.put(cmd)
		if clockform.sync_ww.data:
			print('[frontend][clock] Synching WW')
			cmd='clock-sync-WW'
			frontendqueue.put(cmd)
		if clockform.cal_hh.data:
			print('[frontend][clock] Calibrating HH')
			cmd='clock-cal-HH-' + str(clockform.hh.data).zfill(2)
			frontendqueue.put(cmd)
		if clockform.cal_mm.data:
			print('[frontend][clock] Calibrating MM')
			cmd='clock-cal-MM-' + str(clockform.mm.data).zfill(2)
			frontendqueue.put(cmd)
		if clockform.cal_ww.data:
			print('[frontend][clock] Calibrating WW')
			cmd='clock-cal-WW-' + str(clockform.ww.data).zfill(2)
			frontendqueue.put(cmd)
	
	# Force message to reload queue
	if clockform.calibrating.data:
		frontendqueue.put('clock-calibration-on')
	else:
		frontendqueue.put('clock-calibration-off')


	return render_template('clock.html', cform=clockform)

