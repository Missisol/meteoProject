from datetime import datetime, timezone, date
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class Bme280Rpi(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    temperature: so.Mapped[float] = so.mapped_column(sa.Float)
    humidity: so.Mapped[float] = so.mapped_column(sa.Float)
    pressure: so.Mapped[int] = so.mapped_column(sa.Integer)
    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return '<temperature {}>'.format(self.temperature)
    

class Bme280Outer(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    temperature: so.Mapped[float] = so.mapped_column(sa.Float)
    humidity: so.Mapped[float] = so.mapped_column(sa.Float)
    pressure: so.Mapped[int] = so.mapped_column(sa.Integer)
    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: date.today())
    # date: so.Mapped[datetime] = so.mapped_column(sa.Date, index=True, default=lambda: date.today())
    
    def __repr__(self):
        return f"temperature: {self.temperature}, humidity: {self.humidity}, pressure: {self.pressure}, created_at: {self.created_at}, date: {self.date}"
        

class Dht22(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    temperature1: so.Mapped[float] = so.mapped_column(sa.Float)
    humidity1: so.Mapped[float] = so.mapped_column(sa.Float)
    temperature2: so.Mapped[float] = so.mapped_column(sa.Float)
    humidity2: so.Mapped[float] = so.mapped_column(sa.Float)
    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"temperature-1: {self.temperature1}, humidity-1: {self.humidity1}, temperature-2: {self.temperature2}, humidity-2: {self.humidity2}, created_at: {self.created_at}"


class BmeHistory(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    date: so.Mapped[datetime] = so.mapped_column(
    index=True, default=lambda: date.today())
    min_temperature: so.Mapped[float] = so.mapped_column(sa.Float)
    max_temperature: so.Mapped[float] = so.mapped_column(sa.Float)
    min_humidity: so.Mapped[float] = so.mapped_column(sa.Float)
    max_humidity: so.Mapped[float] = so.mapped_column(sa.Float)
    min_pressure: so.Mapped[int] = so.mapped_column(sa.Integer)
    max_pressure: so.Mapped[int] = so.mapped_column(sa.Integer)

    def __repr__(self):
        return f"date: {self.date}, min temperature: {self.min_temperature}, max temperature: {self.max_temperature}, min humidity: {self.min_humidity}, max humidity: {self.max_humidity}, min pressure: {self.min_pressure}, max pressure: {self.max_pressure}"
