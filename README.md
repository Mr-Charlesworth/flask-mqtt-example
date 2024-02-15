# Flask MQTT Example

- [app.py](./app.py) Contains a small demo integrating mqtt in to flask
- First install flask

```bash
pip install flask
```
 
- We also need flask-mqtt but this installs a dependency which was updated 5 days ago from when I wrote this and 
has breaking changes. So let's install the exact dependency we need first

```bash
pip install paho-mqtt==1.6.1
```

- Now install flask-mqtt

```bash
pip install flask-mqtt
```

- You need to edit the app.config values

```python
app.config['MQTT_BROKER_URL'] = "[ENTER-HIVEMQ-URL-HERE]"  # URL for HiveMQ cluster
app.config['MQTT_USERNAME'] = "[DEFINED-IN-HIVEMQ-CREDENTIALS-FOR-CLUSTER]"  # From the credentials created in HiveMQ
app.config['MQTT_PASSWORD'] = "[DEFINED-IN-HIVEMQ-CREDENTIALS-FOR-CLUSTER]"  # From the credentials created in HiveMQ
app.config['MQTT_CLIENT_ID'] = "[SOME-UNIQUE-CLIENT-ID]"  # Must be unique for any client that connects to the cluster
```