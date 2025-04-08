import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import Bme280Rpi, Bme280Outer, Dht22

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'Bme2800Rpo': Bme280Rpi, 'Bme280Outer': Bme280Outer, 'Dht22': Dht22}


@app.context_processor
def inject_today_date():
    return {'today_date': datetime.date.today()}


@app.context_processor
def getheader_menu():
    return {
        
    }