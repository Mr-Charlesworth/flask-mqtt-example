# Flask MQTT Example

## Forking / Environment stuff
- If you are in GitHub click 'Fork' to copy the repository to your own GitHub
- 'Forking' creates a copy of the repository in your own GitHub repositories space, so you are free to make your own 
changes and push them.
- Once you can see your new copy of the repository in GitHub, click 'Code > SSH > Copy the URL to clipboard'
- Use git-bash to clone your copy of the repository

```bash
git clone [the-url-you-copied]
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
- Ensure you are using credentials that can both publish and subscribe (This is configured in HiveMQ)

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

## The Code in Detail

- We instantiate the Flask app as normal

```python
app = Flask(__name__)
```

- The instance of the Flask app has a config dictionary that we can pass configuration attributes to that are required by flask-mqtt
- Once the Flask app instance has this configuration, we pass the instance to a constructor of the Mqtt client class imported from flask-mqtt

```python
mqtt = Mqtt(app)
```

- As with the flask library, there are lots of things that happen that we don't see (such as the case with any library, we don't want to see them, we just want them to work!)
- Flask wants us to declare route handlers using '@app.route('/some-route')', we don't see the code that listens for and processes requests to these routes, we just need to write them.
- It's the same with flask-mqtt, we can define some handler functions for some expected events such as when the client has connected and when it receives messages to subscribed topics.
- We define a callback handler to do something when we know that the client has connected, that something is printing the connection result and subscribing to a topic

> Note: Connected with result '5' means something has gone wrong, probably incorrect configuration.
> The MQTT Client will continue to attempt to connect in this case and the Flask app will not start.

```python
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt.subscribe("home/test")
```

- We also define a callback handler to do something when a message is received on a subscribed topic. Here that something is simply printing out the message payload to the Flask console.

```python
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(str(message.payload))
```

- We can test the subscription from within Flask by publishing to the same topic
- We do this by writing a simple route on '/publish' that triggers publishing a message on the same topic we subscribed to
- The string that is returned is a reminder to check the Flask console for the message

```python
@app.route('/publish')
def publish_test():
    mqtt.publish('home/test', b'hello???')
    return 'Did it work? (Check your flask console)'
```

>Note: We can't send a response that verifies that the subscription worked. Why not?

## Exercises

1. Create a page in your flask app with a button. Make it so that when the button is pressed it toggles an LED on your pico. Hint: Your pico needs to subscribe to a topic that your flask app publishes to. Another hint: You need to use the same HiveMQ cluster.
2. Create another page in your flask app that shows the status of the LED (on or off). Hint: Make your pico publish to a topic every time it is toggled and subscribe to the same topic in your flask app. Your flask app needs a state to hold the status (i.e. a variable).

## Harder exercise

Take a message as input from a form in your flask app and display it on the LCD display on the pico


