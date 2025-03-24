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


    mqttc = run()
    mqttc.message_callback_add("/bme280/bmereadings", on_message_from_bme280)

    return app

from app import models
from app.sensor.bme280outer import run
