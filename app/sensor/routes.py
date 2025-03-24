from flask import render_template, request, url_for, current_app
from app import db
import sqlalchemy as sa
from app.sensor import bp
from app.models import Bme280, Bme280Outer

from app.sensor.bme280 import BME280Module
bme = BME280Module()


@bp.route('/sensor')
def sensor():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Bme280).order_by(Bme280.created_at.desc())
    data = db.paginate(query, page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    next_url = url_for('sensor.sensor', page=data.next_num) \
        if data.has_next else None
    prev_url = url_for('sensor.sensor', page=data.prev_num) \
        if data.has_prev else None
    return render_template('sensor/bme280_rpi.html', title='BME280', data=data.items, next_url=next_url, prev_url=prev_url)


@bp.route('/sensor-outer')
def sensor_outer():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Bme280Outer).order_by(Bme280Outer.created_at.desc())
    data = db.paginate(query, page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    next_url = url_for('sensor.sensor_outer', page=data.next_num) \
        if data.has_next else None
    prev_url = url_for('sensor.sensor_outer', page=data.prev_num) \
        if data.has_prev else None
    return render_template('sensor/bme280_outer.html', title='BME280 Outer', data=data.items, next_url=next_url, prev_url=prev_url)
