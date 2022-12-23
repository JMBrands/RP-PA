from machine import Pin, ADC
import time as t
adc = ADC(Pin(26))
vls = []
tempold = 0
while True:
    vls.append(adc.read_u16())
    vlav=0
    for val in vls:
        vlav += val
    vlav /= len(vls)
    while len(vls) > 3:
        del vls[0]
    temp = round(abs(vlav-208)/65327*150+100, 0)
    if temp%5 >=2:
        temp += 5-temp%5
    else:
        temp -= temp%5
    temp /= 10
    if tempold != temp:
        print(temp)
    t.sleep(0.5)
    tempold = temp