import ast
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_babel import Babel

def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

def get_timezone():
    return current_app.config['TIMEZONE']


db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)
    babel.init_app(app, locale_selector=get_locale, timezone_selector=get_timezone)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.sensor import bp as sensor_bp
    app.register_blueprint(sensor_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)


    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/meteo.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Meteo startup')


    def on_message_from_bme280(client, userdata, message):
        print(f"{message.topic} {message.payload}")
        if message.topic == app.config['MQTT_TOPIC_BME280']:
            print("BME readings update")
            data = ast.literal_eval(message.payload.decode())
            temperature_val = float(data['temperature'])
            humidity_val = float(data['humidity'])
            pressure_val = round(int(data['pressure']))

            mod = models.Bme280Outer(temperature=temperature_val, humidity=humidity_val, pressure=pressure_val)
            save_on_db(mod)
            socketio.emit('bme_message', message.payload.decode())


    def on_message_from_dht22(client, userdata, message):
        print(f"{message.topic} {message.payload}")
        if message.topic == app.config['MQTT_TOPIC_DHT22']:
            print("DHT readings update")
            data = ast.literal_eval(message.payload.decode())
            temperature_1 = float(data['temperature-1'])
            humidity_1 = float(data['humidity-1'])
            temperature_2 = float(data['temperature-2'])
            humidity_2 = float(data['humidity-2'])

            mod = models.Dht22(temperature1=temperature_1, humidity1=humidity_1, temperature2=temperature_2, humidity2=humidity_2,)
            save_on_db(mod)
            socketio.emit('dht_message', message.payload.decode())


    def save_on_db(data):
        with app.app_context():
            db.session.add(data)
            db.session.commit()


    mqttc = run()
    mqttc.message_callback_add(app.config['MQTT_TOPIC_BME280'], on_message_from_bme280)
    mqttc.message_callback_add(app.config['MQTT_TOPIC_DHT22'], on_message_from_dht22)

    return app

from app import models
from app.sensor.sensor_mqtt import run
