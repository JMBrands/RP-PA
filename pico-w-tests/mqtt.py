from machine import Pin, I2C
import network
import utime
from umqtt.simple import MQTTClient

ssid = "RP4-PA-JMB"
password = "RP4-PA-JMB"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm = 0xa11140) # Diable powersave mode
wlan.connect(ssid, password)

mqtt_server = "gw.wlan"
client_id = "PicoW"
username = "picow"
psswd = "picow"

max_wait = 100
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    utime.sleep(1)

def reconnect():
    print("failed, reconnecting")
    utime.sleep(5)
#Handle connection error
if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')

print('connected')
status = wlan.ifconfig()
print('ip = ' + status[0])
connecting=True
while connecting:
    try:
        client = MQTTClient(client_id, mqtt_server, keepalive=60, user=username, password=psswd)
        client.connect()
        print('Connected to %s MQTT Broker'%(mqtt_server))
        connecting = False
    except OSError as e:
        reconnect()
while True:
    client.publish("test", msg="Hello, World!")
    client.publish("button", msg="0")
    utime.sleep(1)
    client.publish("button", msg="1")
    utime.sleep(1)
    
        