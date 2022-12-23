from gpiozero import GPIODevice
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
pins = []
for p in pinnums:
    pins.append(GPIODevice(p))
cycle=0
while True:
    for i in range(4):
        pins[i].value = steps[cycle][i]