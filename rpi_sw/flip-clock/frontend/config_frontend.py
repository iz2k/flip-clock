from .app import app, frontendqueue
from .config_models import Config, ConfigForm, load_config, save_config
from flask import render_template, request
import os


@app.route('/config', methods=['GET', 'POST'])
def config_index():

	# Load stored config object
	rundir = os.path.dirname(os.path.realpath(__file__))
	cfg = load_config(rundir + '/../config/config.xml')


	if request.method == 'POST':
		reqform = ConfigForm(request.form)
		if reqform.save.data:
			print('[frontend][config] Saving configuration')
			cfg_new = Config(form=reqform)
			if reqform.spotify_pass.data == '':
				cfg_new.spotify_pass = cfg.spotify_pass
			else:
				cfg_new.spotify_pass = reqform.spotify_pass.data
			save_config(config=cfg_new, filename=rundir + '/../config/config.xml')
			#frontendqueue.put('config_update')

	# Load stored config object
	cfg = load_config(rundir + '/../config/config.xml')
		
	# Create config form from object
	cfgform = ConfigForm()
	cfgform.readobject(cfg)

	return render_template('config.html', cform=cfgform)

