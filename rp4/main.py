import paho.mqtt.client as mqtt
import time as t
import re

def check(str_in):
    regex = re.compile("[0-9]+(\.){1}[0-9]+\Z", re.I)
    match = regex.match(str(str_in))
    return bool(match)

def on_connect(client, userdata, flags, rc):
    global loop_flag
    print(f"connected as {client} with {userdata}, {flags}, and {rc}")
    loop_flag = 0

client = mqtt.Client("paho")
client.username_pw_set("picow", "picow")
client.will_set("info", "paho disconnected")
client.on_connect = on_connect
client.connect("192.168.1.24")
client.loop_start()

loop_flag = 1
counter = 0

while loop_flag == 1:
    print("waiting for connection")
    t.sleep(0.1)
    counter += 1

client.subscribe("test")

def on_message(client, userdata, message):
    if check(message.payload.decode()):
        msg = float(message.payload.decode())
        print(msg*10)
    else:
        msg = message.payload.decode()
    print(f"message: \"{msg}\" at: \"{message.topic}\"")

client.on_message = on_message

while True:
    pass
