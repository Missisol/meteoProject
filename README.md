- Install Mosquitto MQTT Broker on Raspberry Pi ``sudo apt install -y mosquitto mosquitto-clients``
- Run app ``flask run --host=0.0.0.0``
- Command for working with the database entities without having to import them ``flask shell``
- Setting up a scheduled job with cron 
    - ``crontab -e``
    - ``* * * * * cd <path_to_project_directory> && .venv/bin/flask <command_name>``
    -  cron need not be
     restarted whenever a crontab file is modified - **[man cron](https://www.manpagez.com/man/8/cron/)**, but ``sudo service cron reload`` 
- Create requirements file``pip freeze > requirements.txt``
- ``pip install -r requirements.txt``
- ``flask db downgrade base`` - when the downgrade command is not given a target, it downgrades one revision. The base target causes all migrations to be downgraded, until the database is left at its initial state, with no tables.

