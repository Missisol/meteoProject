import paho.mqtt.client as mqtt
from app import socketio

broker_url = 'localhost'
broker_port = 1883


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected success")
            client.subscribe('/esp8266/bme280', qos=1)
            client.subscribe('/esp8266/dht22', qos=1)
        else:
            print(f"Connected fail with code {rc}")

    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.connect(broker_url, broker_port, 60)
    return mqttc


def on_message(client, userdata, message):
    print(f"{message.topic} {message.payload}")
    socketio.emit('other_message', message.payload)


def run():
    mqttc = connect_mqtt()
    mqttc.on_message = on_message

    mqttc.loop_start()
    return mqttc

