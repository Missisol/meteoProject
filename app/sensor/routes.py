from flask import render_template, request, url_for, current_app
from app import db
import sqlalchemy as sa
from app.sensor import bp
from app.models import Bme280Rpi, Bme280Outer, Dht22
from flask_babel import format_datetime

# from app.sensor.sensor_rpi import BME280Module
# bme = BME280Module()


@bp.app_template_filter('datetimeformat')
def datetimeformat(value):
    return format_datetime(value, 'd.MM.yyyy, HH:mm:ss')


@bp.route('/bme280-rpi')
def sensor_rpi():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Bme280Rpi).order_by(Bme280Rpi.created_at.desc())
    data = db.paginate(query, page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    next_url = url_for('sensor.sensor_rpi', page=data.next_num) \
        if data.has_next else None
    prev_url = url_for('sensor.sensor_rpi', page=data.prev_num) \
        if data.has_prev else None
    return render_template('sensor/bme280_rpi.html', title='BME280 RPI', data=data.items, next_url=next_url, prev_url=prev_url)


@bp.route('/bme280-outer')
def bme280_outer():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Bme280Outer).order_by(Bme280Outer.created_at.desc())
    data = db.paginate(query, page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    next_url = url_for('sensor.bme280_outer', page=data.next_num) \
        if data.has_next else None
    prev_url = url_for('sensor.bme280_outer', page=data.prev_num) \
        if data.has_prev else None
    return render_template('sensor/bme280_outer.html', title='BME280 Outer', data=data.items, next_url=next_url, prev_url=prev_url)


@bp.route('/dht22-outer')
def dht22_outer():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Dht22).order_by(Dht22.created_at.desc())
    data = db.paginate(query, page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    next_url = url_for('sensor.dht22_outer', page=data.next_num) \
        if data.has_next else None
    prev_url = url_for('sensor.dht22_outer', page=data.prev_num) \
        if data.has_prev else None
    return render_template('sensor/dht22_outer.html', title='DHT22 Outer', data=data.items, next_url=next_url, prev_url=prev_url)
