#!/bin/bash
flask db upgrade
exec gunicorn -k gevent -b 0.0.0.0:5000 --access-logfile - --error-logfile - meteo:app