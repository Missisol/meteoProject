from datetime import datetime, timezone, date
from flask import render_template, request, url_for, jsonify
from app import db
import sqlalchemy as sa
from app.main import bp
from app.sensor.sensor_rpi import BME280Module
from app.models import Bme280Outer, Dht22
from app.utils.sensor_data import list_bme, list_dht, prefix_list

bme = BME280Module()


@bp.route('/')
@bp.route('/home')
def index():
    return render_template('home.html', title='Home')


@bp.route('/bme280Rpi')
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
    query = sa.select(Bme280Outer).order_by(Bme280Outer.created_at.desc())
    data = db.session.scalar(query)
    if data:
        return jsonify(
            {
                'temperature': data.temperature,
                'humidity': data.humidity,
                'pressure': data.pressure,
                'created_at': data.created_at,
                'date': data.date,
            }
        )
    else:
        return jsonify(
            {
                'temperature': '-',
                'humidity': '-',
                'pressure': '-',
                'created_at': datetime.now(),
                'date': date.today(),
            }
        )


@bp.route('/dht22Outer')
def get_dht_mqtt_data():
    query = sa.select(Dht22).order_by(Dht22.created_at.desc())
    data = db.session.scalar(query)
    if data:
        return jsonify(
            {
                'temperature1': data.temperature1,
                'humidity1': data.humidity1,
                'temperature2': data.temperature2,
                'humidity2': data.humidity2,
                'created_at': data.created_at,
            }
        )
    else:
        return jsonify(
            {
                'temperature1': '-',
                'humidity1': '-',
                'temperature2': '-',
                'humidity2': '-',
                'created_at': datetime.now(),
            }
        )


@bp.app_context_processor
def inject_boxes():
    return dict(
        {
            'bme_list': list_bme,
            'dht_list': list_dht,
            'prefix_list': prefix_list,
        }
    )