from flask import render_template, request, url_for, jsonify
from app import db
import sqlalchemy as sa
from app.main import bp
from app.sensor.sensor_rpi import BME280Module
from app.models import Bme280Outer, Dht22
from app.utils.sensor_data import box4, box5
bme = BME280Module()


@bp.route('/')
@bp.route('/home')
def index():
    return render_template('home.html', title='Home')


@bp.route('/sensorReadings')
def get_sensor_readings():
    temperature, pressure, humidity, created_at = bme.get_sensor_readings()
    return jsonify(
        {
            "status": "OK",
            "temperature": temperature,
            "pressure": pressure,
            "humidity": humidity,
            "created_at": created_at,
        }
    )


@bp.route('/bme280Outer')
def get_bme_mqtt_data():
    data = Bme280Outer.query.order_by(Bme280Outer.created_at.desc()).first()
    # query = sa.select(Bme280Outer).order_by(Bme280Outer.created_at.desc()).limit(1)
    # data = db.session.scalars(query)
    return jsonify(
        {
            'temperature': data.temperature,
            'humidity': data.humidity,
            'pressure': data.pressure,
            'created_at': data.created_at,
        }
    )


@bp.route('/dht22Outer')
def get_dht_mqtt_data():
    data = Dht22.query.order_by(Dht22.created_at.desc()).first()
    return jsonify(
        {
            'temperature1': data.temperature1,
            'humidity1': data.humidity1,
            'temperature2': data.temperature2,
            'humidity2': data.humidity2,
            'created_at': data.created_at,
        }
    )


@bp.app_context_processor
def inject_boxes():
    return dict(
        {
            'bme_list': box5,
            'dht_list': box4
        }
    )