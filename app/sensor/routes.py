from datetime import datetime, date
from flask import render_template, request, url_for, current_app, jsonify
from app import db
import sqlalchemy as sa
from app.sensor import bp
from app.models import Bme280Rpi, Bme280Outer, Dht22, BmeHistory
from app.utils.sensor_data import bme_rpi_table, bme_outer_table, dht_outer_table, history_table
from flask_babel import format_datetime

from app.sensor.sensor_rpi import BME280Module
bme = BME280Module()


@bp.app_template_filter('datetimeformat')
def datetimeformat(value):
    return format_datetime(value, 'd.MM.yyyy, HH:mm:ss')
    # return datetime.strftime(value, '%d.%m.%y - %H:%M:%S')

@bp.app_template_filter('dateformat')
def dateformat(value):
    return format_datetime(value, 'd.MM.yyyy')
    # return datetime.strftime(value, '%d.%m.%y')


@bp.route('/sensors')
def sensors():
    return render_template('sensor/sensors_data.html', title='Sensors')


@bp.route('/bme280_rpi')
def bme280_rpi():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Bme280Rpi).order_by(Bme280Rpi.created_at.desc())
    data = db.paginate(query, page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    next_url = url_for('sensor.bme280_rpi', page=data.next_num) \
        if data.has_next else None
    prev_url = url_for('sensor.bme280_rpi', page=data.prev_num) \
        if data.has_prev else None
    return render_template('sensor/sensor_table.html', title='BME280 RPI', data=data.items, next_url=next_url, prev_url=prev_url, table=bme_rpi_table)


@bp.route('/bme280_outer')
def bme280_outer():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Bme280Outer).order_by(Bme280Outer.created_at.desc())
    data = db.paginate(query, page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    next_url = url_for('sensor.bme280_outer', page=data.next_num) \
        if data.has_next else None
    prev_url = url_for('sensor.bme280_outer', page=data.prev_num) \
        if data.has_prev else None
    return render_template('sensor/sensor_table.html', title='BME280 внешний', data=data.items, next_url=next_url, prev_url=prev_url, table=bme_outer_table)


@bp.route('/dht22_outer')
def dht22_outer():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Dht22).order_by(Dht22.created_at.desc())
    data = db.paginate(query, page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    next_url = url_for('sensor.dht22_outer', page=data.next_num) \
        if data.has_next else None
    prev_url = url_for('sensor.dht22_outer', page=data.prev_num) \
        if data.has_prev else None
    return render_template('sensor/sensor_table.html', title='DHT22', data=data.items, next_url=next_url, prev_url=prev_url, table=dht_outer_table)


@bp.route('/bme_history')
def bme_history():
    page = request.args.get('page', 1, type=int)
    query = sa.select(BmeHistory).order_by(BmeHistory.date.desc())
    data = db.paginate(query, page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)   
    # data = db.session.scalars(query)
    next_url = url_for('sensor.bme_history', page=data.next_num) \
        if data.has_next else None
    prev_url = url_for('sensor.bme_history', page=data.prev_num) \
        if data.has_prev else None
    return render_template('sensor/sensor_table.html', title='BME280 история', data=data.items, next_url=next_url, prev_url=prev_url, table=history_table)


@bp.route('/json_history', methods=['GET', 'POST'])
def json_history():
    start = request.args.get('start')
    end = request.args.get('end')
    print(f'params: {start} and {end}')

    if start and end:
        print('start', date.fromisoformat(start))
        print('end', date.fromisoformat(end))
        query = sa.select(BmeHistory).filter(BmeHistory.date >= date.fromisoformat(start), BmeHistory.date <= date.fromisoformat(end)).order_by(BmeHistory.date.desc())
    else:
        query = sa.select(BmeHistory).order_by(BmeHistory.date.desc()).limit(current_app.config['HISTORY_ITEMS_LIMIT'])
    data = db.session.scalars(query)

    if data:
        return [{
                'min_temperature': n.min_temperature,
                'max_temperature': n.max_temperature, 
                'min_humidity': n.min_humidity,
                'max_humidity': n.max_humidity, 
                'min_pressure': n.min_pressure, 
                'max_pressure': n.max_pressure, 
                'date': n.date,
            } for n in data]
    else:
        return {}


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

