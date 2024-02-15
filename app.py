from flask import Flask
from flask_mqtt import Mqtt
import ssl

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = "[ENTER-HIVEMQ-URL-HERE]"  # URL for HiveMQ cluster
app.config['MQTT_USERNAME'] = "[DEFINED-IN-HIVEMQ-CREDENTIALS-FOR-CLUSTER]"  # From the credentials created in HiveMQ
app.config['MQTT_PASSWORD'] = "[DEFINED-IN-HIVEMQ-CREDENTIALS-FOR-CLUSTER]"  # From the credentials created in HiveMQ
app.config['MQTT_CLIENT_ID'] = "[SOME-UNIQUE-CLIENT-ID]"  # Must be unique for any client that connects to the cluster
app.config['MQTT_BROKER_PORT'] = 8883  # MQTT port for encrypted traffic
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = True
app.config['MQTT_TLS_INSECURE'] = False
app.config['MQTT_TLS_CA_CERTS'] = 'isrgrootx1.pem'  # CA for HiveMQ, read: https://letsencrypt.org/about/
app.config['MQTT_TLS_VERSION'] = ssl.PROTOCOL_TLSv1_2
app.config['MQTT_TLS_CIPHERS'] = None

# Instantiate the mqtt client object (requires instance of flask app as param)
mqtt = Mqtt(app)


# Define a callback to be called when the mqtt client connects
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt.subscribe("home/test")  # We are subscribing to the 'home/test' topic which we made up here


# Define a callback for when a message is received on a subscribed topic
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(str(message.payload))
    print(client)
    print(userdata)


# A simple route to fire off publishing a message (we use this to test if it is working)
@app.route('/publish')
def publish_test():
    mqtt.publish('home/test', b'hello???')
    return 'Did it work? (Check your flask console)'


if __name__ == '__main__':
    app.run(debug=True)
