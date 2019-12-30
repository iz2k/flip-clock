#!/usr/bin/python3

from app import app
import radio_frontend
import alarm_frontend
import spotify_frontend

if __name__ == '__main__':
	import os

	if 'WINGDB_ACTIVE' in os.environ:
		app.debug = False
	app.run(port=5000, host='0.0.0.0')
