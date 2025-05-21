FROM python:3.11-slim

# WORKDIR /app
# COPY requirements.txt .

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn gevent

# This command will also copy the SQLite database
# COPY . .

COPY app app
COPY migrations migrations
COPY meteo.py config.py boot.sh ./
RUN chmod a+x boot.sh


ENV FLASK_APP=meteo.py
RUN flask

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]


