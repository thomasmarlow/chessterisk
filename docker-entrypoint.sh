#!/bin/bash

sleep 5

export FLASK_APP=server
flask db init
flask db migrate
flask db upgrade

sleep 5

gunicorn -k "eventlet" -w 1 -b 0.0.0.0:5000 server:app

