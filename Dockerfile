FROM python:3.11-slim

# WORKDIR /app
COPY requirements.txt requirements.txt
# COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn gevent

# COPY . .
COPY app app
COPY migrations migrations
# COPY meteo.py config.py ./
COPY meteo.py config.py boot.sh .flaskenv ./
RUN chmod a+x boot.sh


ENV FLASK_APP=meteo.py
RUN flask

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
# CMD ["gunicorn", "-b", "0.0.0.0", "meteo:app"]
# CMD ["gunicorn", "-k", "gevent", "-b", "0.0.0.0", "meteo:app"]
# CMD ["gunicorn", "-k", "gevent", "-b", "0.0.0.0:8000", "meteo:app"]
# CMD ["gunicorn", "-k", "gevent", "-w", "1",  "-b", "0.0.0.0:8000", "meteo:app"]
# CMD ["gunicorn", "--worker-class", "gevent", "-b", "0.0.0.0", "--timeout", "5", "meteo:app"]


