from wtforms import Form, StringField, BooleanField, SelectField, DecimalField, SubmitField, HiddenField, IntegerField

class FClockForm(Form):
	hh = IntegerField('HH', render_kw={"placeholder": "HH", "style":"font-size:20px", "size":"1"})
	mm = IntegerField('MM', render_kw={"placeholder": "MM", "style":"font-size:20px", "size":"1"})
	ww = IntegerField('WW', render_kw={"placeholder": "WW", "style":"font-size:20px", "size":"1"})
	calibrating = BooleanField('Calibrating', render_kw={"onchange":"document.getElementById('clockform').submit()"})
	set_hh = SubmitField(label='Set HH')
	set_mm = SubmitField(label='Set MM')
	set_ww = SubmitField(label='Set WW')
	sync_hh = SubmitField(label='Sync HH')
	sync_mm = SubmitField(label='Sync MM')
	sync_ww = SubmitField(label='Sync WW')
	cal_hh = SubmitField(label='Cal HH')
	cal_mm = SubmitField(label='Cal MM')
	cal_ww = SubmitField(label='Cal WW')
	