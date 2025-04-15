from datetime import date, timedelta, datetime
from flask import current_app
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import Bme280Outer, BmeHistory


def get_minmax_bme_data():
    for x in range(1, current_app.config['DAYS_RANGE'], 1):
        print(f'x: {x}')
        day = date.today() - timedelta(days=x) 
        print(f"date day: {day}")

        bq = sa.select(Bme280Outer).filter(sa.func.DATE(Bme280Outer.created_at) == day)
        bme_earlier_data = db.session.scalars(bq).first()

        hq = sa.select(BmeHistory).filter(sa.func.DATE(BmeHistory.date) == day)
        history_earlier_data = db.session.scalars(hq).first()

        try:
            if bme_earlier_data and not history_earlier_data:
                inner_query = sa.select(Bme280Outer).filter(sa.func.DATE(Bme280Outer.created_at) == day).order_by(Bme280Outer.created_at.desc())
                subq = inner_query.subquery()
                minmax = so.aliased(Bme280Outer, subq)
                u = sa.select(
                    sa.func.min(minmax.temperature),
                    sa.func.max(minmax.temperature),
                    sa.func.min(minmax.humidity),
                    sa.func.max(minmax.humidity),
                    sa.func.min(minmax.pressure),
                    sa.func.max(minmax.pressure),
                    sa.func.DATE(minmax.created_at)
                )

                history = sa.insert(BmeHistory).from_select(['min_temperature', 'max_temperature', 'min_humidity', 'max_humidity', 'min_pressure', 'max_pressure', 'date'], u)

                db.session.execute(history)
                db.session.commit()

                delete_model_data(Bme280Outer, x)

            elif bme_earlier_data and history_earlier_data:
                delete_model_data(Bme280Outer, x)
            else:
                print('BME data has already been deleted')

        except Exception as e:
            print(e)



def delete_history_data(days):
    day = date.today() - timedelta(days=days) 
    del_stmt = sa.delete(BmeHistory).where(sa.func.DATE(BmeHistory.date) == day)

    db.session.execute(del_stmt)
    db.session.commit()


def delete_model_data(model, days):
    day = date.today() - timedelta(days=days) 
    del_stmt = sa.delete(model).filter(sa.func.DATE(model.created_at) == day)

    db.session.execute(del_stmt)
    db.session.commit()


def clear_db(model):
    for x in range(1, current_app.config['DAYS_RANGE'], 1):
        delete_model_data(model, x)
