from flask import Flask, request
import paho.mqtt.client as mqtt

#HTTP
HTTP_SERVER_PORT = 5001
#MQTT
MQTT_SERVER_IP = "localhost"
MQTT_SERVER_PORT = 1883

app = Flask(__name__)
mqtt_client = mqtt.Client()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all_path(path):
    message = request.args.get('m')
    if message != None:
        send_message('/' + path,  message)
        return "0"
    else:
        return "-1"

def send_message(topic, message):
    print("Sending message '{}' to '{}'".format(message, topic))
    mqtt_client.publish(topic, payload=message, qos=0, retain=False)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT server '{}:{}' with result code '{}'".format(MQTT_SERVER_IP, MQTT_SERVER_PORT, str(rc)))

if __name__ == "__main__":
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(MQTT_SERVER_IP, MQTT_SERVER_PORT, 60)
    mqtt_client.loop_start()
    app.run(host='0.0.0.0', port=HTTP_SERVER_PORT)
