# from app import mqtt

# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print('Connected successfully')
#         mqtt.subscribe('/bme280/bmereadings')
#     else:
#         print('Bad connection. Code:', rc)

# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, message):
#     print(f"{message.topic} {message.payload}")
#     if message.topic == "/bme280/bmereadings":
#         print("BME readings update")

#     data = dict(
#         topic=message.topic,
#         payload=message.payload.decode()
#     )
#     print('Received message on topic: {topic} with payload: {payload}'.format(**data))

# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
#     print(level, buf)


# import ast
# from datetime import datetime, timezone


# from app import db

# from app.models import Bme280Outer


import paho.mqtt.client as mqtt


broker_url = 'localhost'
broker_port = 1883


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected success")
        else:
            print(f"Connected fail with code {rc}")

    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.connect(broker_url, broker_port, 60)
    return mqttc

def on_message(client, userdata, message):
    print("Message Recieved from DHT22: "+message.payload.decode())

def run():
    mqttc = connect_mqtt()
    mqttc.on_message = on_message
    mqttc.subscribe("/bme280/bmereadings", qos=1)
    mqttc.subscribe("/dht22/dhtreadings", qos=1)

    mqttc.loop_start()
    return mqttc





# def on_message(client, userdata, message):
#     print(f"{message.topic} {message.payload}")
#     if message.topic == "/bme280/bmereadings":
#         print("BME readings update")
#         # print(f"{message.payload.decode()}")
#         data = ast.literal_eval(message.payload.decode())
#         print(data)
#         print(float(data['temperature']))
#         temperature_val = float(data['temperature'])
#         humidity_val = float(data['humidity'])
#         pressure_val = round(int(data['pressure']))

#         data = Bme280Outer(temperature=temperature_val, humidity=humidity_val, pressure=pressure_val)


#         db.session.add(data)
#         db.session.commit()


# mqttc=mqtt.Client()
# mqttc.on_connect = on_connect
# mqttc.on_message = on_message
# mqttc.connect("localhost",1883,60)
# mqttc.loop_start()


