import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import Bme280, Bme280Outer

app = create_app()


@app.shell_context_processor
def make_shell_context():
  return {'sa': sa, 'so': so, 'db': db, 'Bme2800': Bme280, 'Bme280Outer': Bme280Outer}