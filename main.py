import machine
import sys
import time
import json
from servo import Servo

laser_pin = machine.Pin(28, machine.Pin.OUT)
onboard_led = machine.Pin(25, machine.Pin.OUT)

pan = Servo(pin=27)
tilt = Servo(pin=26)

onboard_led.toggle()
time.sleep(0.1)
onboard_led.toggle()
time.sleep(0.1)
onboard_led.toggle()
time.sleep(0.1)

print("MR ZAPPY ONLINE")
pan.move(90)
tilt.move(90)
def control(payload):
    
    laser_pin.value(payload["laser"])
    pan.move(payload["pan"])
    tilt.move(payload["tilt"])
    #print(payload)

while True:
    
    v = sys.stdin.readline().strip()
    print(v)
    try:
        payload = json.loads(v)
        control(payload)
    except Exception:
        pass

