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

    from app.pwa import bp as pwa_bp
    app.register_blueprint(pwa_bp)


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
            socketio.emit('bme_message', message.payload.decode())

            data = ast.literal_eval(message.payload.decode())
            # if int(data['pressure']) > 0:
            temperature_val = float(data['temperature'])
            humidity_val = float(data['humidity'])
            pressure_val = round(int(data['pressure']))

            if temperature_val < 100 and humidity_val != 100 and pressure_val > 0 and pressure_val < 800:
                mod = models.Bme280Outer(temperature=temperature_val, humidity=humidity_val, pressure=pressure_val)
                save_on_db(mod)
            else:
                print('Sensor data error for saving')


    def on_message_from_dht22(client, userdata, message):
        print(f"{message.topic} {message.payload}")
        if message.topic == app.config['MQTT_TOPIC_DHT22']:
            print("DHT readings update")
            socketio.emit('dht_message', message.payload.decode())

            data = ast.literal_eval(message.payload.decode())
            temperature_1 = float(data['temperature1'])
            humidity_1 = float(data['humidity1'])
            temperature_2 = float(data['temperature2'])
            humidity_2 = float(data['humidity2'])

            mod = models.Dht22(temperature1=temperature_1, humidity1=humidity_1, temperature2=temperature_2, humidity2=humidity_2,)
            save_on_db(mod)


    def save_on_db(data):
        with app.app_context():
            db.session.add(data)
            db.session.commit()


    mqttc = connect_mqtt()
    mqttc.message_callback_add(app.config['MQTT_TOPIC_BME280'], on_message_from_bme280)
    mqttc.message_callback_add(app.config['MQTT_TOPIC_DHT22'], on_message_from_dht22)

    return app

from app import models
from app.sensor.sensor_mqtt import connect_mqtt
