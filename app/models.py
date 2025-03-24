from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Bme280(db.Model):
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
    
    def __repr__(self):
        return '<temperature outer {}>'.format(self.temperature)