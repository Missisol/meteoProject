import ast
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import paho.mqtt.client as mqtt


db = SQLAlchemy()
migrate = Migrate()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

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


    # broker_url = 'localhost'
    # broker_port = 1883

    # def on_connect(client, userdata, flags, rc):
    #     if rc == 0:
    #         print("Connected success")
    #     else:
    #         print(f"Connected fail with code {rc}")
    #     # Subscribing in on_connect() means that if we lose the connection and
    #     # reconnect then subscriptions will be renewed.


    # def on_message(client, userdata, message):
    def on_message_from_bme280(client, userdata, message):
        print(f"{message.topic} {message.payload}")
        if message.topic == "/bme280/bmereadings":
            print("BME readings update")
            data = ast.literal_eval(message.payload.decode())
            temperature_val = float(data['temperature'])
            humidity_val = float(data['humidity'])
            pressure_val = round(int(data['pressure']))

            data = models.Bme280Outer(temperature=temperature_val, humidity=humidity_val, pressure=pressure_val)

            with app.app_context():
                db.session.add(data)
                db.session.commit()


    # mqttc=mqtt.Client()
    # mqttc.on_connect = on_connect
    # mqttc.on_message = on_message
    # # mqttc.on_subscribe = on_subscribe
    # mqttc.connect(broker_url, broker_port, 60)
    # # mqttc.connect("localhost", 1883, 60)
    # mqttc.subscribe("/bme280/bmereadings", qos=1)
    # mqttc.subscribe("/dht22/dhtreadings", qos=1)

    # mqttc.loop_start()

    mqttc = run()
    mqttc.message_callback_add("/bme280/bmereadings", on_message_from_bme280)

    return app

from app import models
from app.sensor.bme280outer import run
