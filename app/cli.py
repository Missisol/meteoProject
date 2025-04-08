import time
from flask import Blueprint

bp = Blueprint('cli', __name__, cli_group=None)
# bp = Blueprint('cli', __name__)



from app.sensor.sensor_rpi import BME280Module
bme = BME280Module()

from app.sensor.sensor_history import get_minmax_bme_data


# @bp.cli.group()
# def scheduled():
#     """Job"""
#     pass

# @scheduled.command()
# def bme280():
#     """Init bme"""
#     print('Start job')
#     bme.get_sensor_readings()
#     time.sleep(5)
#     print('End job')

@bp.cli.command()
def scheduled():
    """Init sensor"""
    print('Sheduled')
    bme.save_sensor_readings()
    # get_minmax_bme_data()


