from gpiozero import DigitalOutputDevice
import time as t
pinnums = [26, 19, 13, 6]
steps = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]
steps_full = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
    ]
pins = []
for p in pinnums:
    pins.append(DigitalOutputDevice(p))
cycle=0
cycletot=0
while True:
    if cycletot < 2048:
        for i in range(4):
            pins[i].value = steps_full[cycle][i]
    else:
        for i in range(4):
            pins[i].value = steps_full[3-cycle][i]
    t.sleep(0.002)
    cycle = (cycle +1)%4
    cycletot = (cycletot+1)%4096