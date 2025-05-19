import paho.mqtt.client as mqtt
from app import socketio

broker_url = '192.168.1.122'
broker_port = 1883


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
        client.subscribe('/esp8266/bme280', qos=1)
        client.subscribe('/esp8266/dht22', qos=1)
    else:
        print(f"Connected fail with code {rc}")


def on_message(client, userdata, message):
    print(f"{message.topic} {message.payload}")
    socketio.emit('other_message', message.payload)


def connect_mqtt():
    mqttc = mqtt.Client()
    print('mqtt')
    print(mqttc)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.connect(broker_url, broker_port, 60)
    mqttc.loop_start()
    return mqttc
