import machine
import onewire
import ds18x20
import time as t
import network
import network
from umqtt.simple import MQTTClient
import _thread as threading
from ssd1306 import SSD1306_I2C
print("hi1")
ds_pin = machine.Pin(16)
print("hi1")
btn = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)
print("hi1")
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
print("hi1")
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))
print("hi1")
i2c.scan()
print("hi1")
#oled = SSD1306_I2C(128, 64, i2c)
print("hi2")
ssid = "RP4-PA-JMB"
password = "RP4-PA-JMB"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm=0xa11140)  # Diable powersave mode
wlan.connect(ssid, password)
print("hi")
mqtt_server = "gw.wlan"
client_id = "PicoW"
username = "picow"
psswd = "picow"
roms = ds_sensor.scan()
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    t.sleep(1)

print(1)


def reconnect():
    print("failed, reconnecting")
    t.sleep(5)


def potmeter():
    adc = machine.ADC(machine.Pin(26))
    vls = []
    tempold = 0
    while True:
        vls.append(adc.read_u16())
        vlav = 0
        for val in vls:
            vlav += val
        vlav /= len(vls)
        while len(vls) > 3:
            del vls[0]
        temp = round(abs(vlav-208)/65327*150+100, 0)
        if temp % 5 >= 2:
            temp += 5-temp % 5
        else:
            temp -= temp % 5
        temp /= 10
        if tempold != temp:
            print(temp)
        t.sleep(0.5)
        tempold = temp


print(2)
print('Found DS devices: ', roms)
if wlan.status() != 3:
#    pass
    raise RuntimeError('wifi connection failed')
connecting = True
while connecting:
    try:
        client = MQTTClient(client_id, mqtt_server,
                            keepalive=60, user=username, password=psswd)
        client.connect()
        print('Connected to %s MQTT Broker' % (mqtt_server))
        connecting = False
    except OSError as e:
        reconnect()
client
print(3)
# potm = threading.start_new_thread(potmeter())
# potm.start()
i = 0
adc = machine.ADC(machine.Pin(26))
vls = []
tempold = 0
btnold = 0
temperature=0
while True:
    if i == 0:
        ds_sensor.convert_temp()
        #oled.text(f"{temperature}",0,0,0)
        temperature= ds_sensor.read_temp(roms[0])
        t.sleep_ms(750)
        client.publish("temp", msg=f"{temperature}")
        #oled.text(f"{temperature}",0,0)
    i += 1
    i = i % 20
    vls.append(adc.read_u16())
    vlav = 0
    for val in vls:
        vlav += val
    vlav /= len(vls)
    while len(vls) > 3:
        del vls[0]
    temp = round(abs(vlav-208)/65327*100+150, 0)
    if temp % 5 >= 2:
        temp += 5-temp % 5
    else:
        temp -= temp % 5
    temp /= 10
    if tempold != temp:
        client.publish("pot", msg=f"{temp}")
        #oled.text(f"{tempold}",0,30,0)
        #oled.text(f"{temp}",0,30)
        tempold = temp
    btnval = btn.value()
    if btnval != btnold:
        client.publish("btn", msg=f"{btnval}")
        #oled.text(f"{btnold}",0,45,0)
        btnold = btnval
        #oled.text(f"{btnval}",0,45)
    #oled.show()
    t.sleep(0.5)
 