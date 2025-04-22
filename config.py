import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    LANGUAGES = ['ru', 'en']
    TIMEZONE = 'Europe/Moscow'
    ITEMS_PER_PAGE = 16
    MQTT_TOPIC_BME280 = '/esp8266/bme280'
    MQTT_TOPIC_DHT22 = '/esp8266/dht22'
    DAYS_RANGE = 11

