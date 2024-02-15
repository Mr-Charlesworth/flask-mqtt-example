# Flask MQTT Example

## Forking / Environment stuff
- If you are in GitHub click 'Fork' to copy the repository to your own GitHub
- 'Forking' creates a copy of the repository in your own GitHub repositories space, so you are free to make your own 
changes and push them.
- Once you can see your new copy of the repository in GitHub, click 'Code > SSH > Copy the URL to clipboard'
- Use git-bash to clone your copy of the repository

```bash
git clone [the-url-you-copied-not]
```
- Now open the cloned directory in PyCharm
- To ensure we are working in an environment that is not using global python packages, and we can install what we want, 
we need to use a virtual environment
- Click the [python interpreter selector](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html#widget) (bottom right corner in PyCharm)
- Choose "Add New Interpreter" > "Add Local Interpreter"
- In the left-hand pane of the Add Python Interpreter dialog, select Virtualenv Environment.
- The default location should be a folder called "venv" inside your project folder
- Now when we install packages, we install them in an isolated environment, which is good.
- Use the terminal in PyCharm as this will use the environment we just created.
- If you already have a terminal open, open a new one to be sure it is using the environment.

## Installing Dependencies

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
- Ensure you are using credentials that can both publish and subscribe

```python
app.config['MQTT_BROKER_URL'] = "[ENTER-HIVEMQ-URL-HERE]"  # URL for HiveMQ cluster
app.config['MQTT_USERNAME'] = "[DEFINED-IN-HIVEMQ-CREDENTIALS-FOR-CLUSTER]"  # From the credentials created in HiveMQ
app.config['MQTT_PASSWORD'] = "[DEFINED-IN-HIVEMQ-CREDENTIALS-FOR-CLUSTER]"  # From the credentials created in HiveMQ
app.config['MQTT_CLIENT_ID'] = "[SOME-UNIQUE-CLIENT-ID]"  # Must be unique for any client that connects to the cluster
```

- The example creates an MQTT client that runs alongside the Flask web server
- We can subscribe to topics and define a callback that fires when a message is received on a subscribed topic
- This example also publishes to the same topic which we can trigger by going to [http://localhost:5000/publish](http://localhost:5000/publish)
- We should then be able to see the message in the flask server console