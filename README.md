- Установка mosquitto broker
- Запуск ```flask run --host=0.0.0.0```
- ```flask shell```
- Запуск redis-server ```sudo service redis-server start```
- Проверка статуса redis-server ```sudo service redis-server status```
- Запуск воркера ```rq worker <task-name>```
- ```crontab -e```
```* * * * * cd /home/marina/Projects/meteoProject && .venv/bin/flask scheduled```

