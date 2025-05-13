***[Project on Github](https://github.com/Missisol/meteoProject/tree/develop)***

***[Sketches on Github](https://github.com/Missisol/ESP8266_BME280_DHT22_project)*** - скетчи для ESP8266 с BME280 и DHT22

---

### Настройка проекта
- Создание виртуальной среды - `python3 -m venv <env name>`
- Активация витруальной среды - `source <env name>/bin/activate`
- Установка зависимостей - `pip install -r requirements.txt`
- [Mosquitto Brocker settings](https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/)
    - установка Mosquitto Broker на Raspberry Pi
    `sudo apt install -y mosquitto mosquitto-clients`
    - настройка автоматического запуска Mosquitto Broker при загрузке RPI - `sudo systemctl enable mosquitto.service`
- Запуск проекта в dev режиме - `flask run --host=0.0.0.0`
- Настройка расписания выполнения задач с использованием Cron 
    - `crontab -e`
    - `* * * * * cd <path_to_project_directory> && <env name>/bin/flask <command_name>`

---

### Прод
- создать файл mosquitto.conf в домашней директории
- контейнеризация Mosquitt MQTT Broker - [How to Configure Mosquitto MQTT Broker in Docker](https://cedalo.com/blog/mosquitto-docker-configuration-ultimate-guide/) - `docker run -itd --rm --name <name> -p 1883:1883 -v $HOME/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto:2`
- Деплой [Setting Up Gunicorn and Supervisor](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux)
    - установить supervisor - sudo apt install supervisor
    - создать файл конфигурации supervisor /etc/supervisor/conf.d/meteo.conf
        [program:meteo]
        command=/<path-to-project>/.venv/bin/gunicorn -k gevent -b 0.0.0.0:8000 meteo:app
        directory=/<path-to-project>
        user=<username>
        autostart=true
        autorestart=true
        stopasgroup=true
        killasgroup=true
    - `sudo supervisorctl reload`


---

#### Команды
- Command for working with the database entities without having to import them `flask shell`
- Create requirements file - `pip freeze > requirements.txt`
- `flask db downgrade base` - when the downgrade command is not given a target, it downgrades one revision. The base target causes all migrations to be downgraded, until the database is left at its initial state, with no tables.

---

#### Полезные ссылки
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Flask regularly scheduled jobs with Cron](https://blog.miguelgrinberg.com/post/run-your-flask-regularly-scheduled-jobs-with-cron)
- [ESP8266 Publishing DHT22 Readings with MQTT to Raspberry Pi](https://randomnerdtutorials.com/esp8266-publishing-dht22-readings-with-mqtt-to-raspberry-pi/)
- [crontab guru](https://crontab.guru/)
-  cron need not be
    restarted whenever a crontab file is modified - [man cron](https://www.manpagez.com/man/8/cron/), but `sudo service cron reload`

