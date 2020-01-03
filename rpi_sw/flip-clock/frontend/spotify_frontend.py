from .app import app, frontendqueue
from .spotify_models import Spotitem, SpotitemForm, save_spotitem_list, load_spotitem_list
from flask import render_template, request
import os


@app.route('/spotify', methods=['GET', 'POST'])
def spotify_index():
	# Load stored spotitem objects
	rundir = os.path.dirname(os.path.realpath(__file__))
	spotitems = load_spotitem_list(rundir + '/../config/spotify.xml')

	if request.method == 'POST':
		reqform = SpotitemForm(request.form)
		if reqform.new.data:
			print('[frontend][spotify] Adding new spotitem')
			spotitem = Spotitem(form=reqform)
			spotitems.append(spotitem)
		if reqform.update.data:
			print('[frontend][spotify] Updating spotitem')
			spotitems[int(reqform.idx.data)].parseForm(reqform)
		if reqform.delete.data:
			print('[frontend][spotify] Deleting spotitem')
			spotitems.pop(int(reqform.idx.data))
		save_spotitem_list(spotitems=spotitems, filename=rundir + '/../config/spotify.xml')
		frontendqueue.put('spotify_update')

	# Create spotitem forms from objects
	spotitemforms=[]
	for idx, el in enumerate(spotitems):
		spotitemform = SpotitemForm()
		spotitemform.readobject(el)
		spotitemform.idx.data=idx
		spotitemforms.append(spotitemform)

	return render_template('spotify.html', sforms=spotitemforms, nsforms=len(spotitemforms), sformnew=SpotitemForm())

