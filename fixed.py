import serial
import json
import time

class turret_serial:
    TERMINATOR = '\r'.encode('UTF8')

    def __init__(self):
        self.serial = serial.Serial('COM4', 115200)

    def send(self, text: str):
        line = '%s\r\f' % text
        self.serial.write(line.encode('utf-8'))
        reply = self.receive()
        print(reply)

    def close(self):
        self.serial.close()

    def receive(self) -> str:
        line = self.serial.read_until(self.TERMINATOR)
        return line.decode('UTF8').strip()

turret = turret_serial()

payload = {
    "laser": False,
    "pan":1500,
    "tilt":1501
}
for i in range(1, 100):
    if i % 2:
        payload = {
                "laser": False,
                "pan":45,
                "tilt":45
            }
    else:
        payload = {
                "laser": True,
                "pan":135,
                "tilt":135
          }
    time.sleep(1)
    print(i)
    turret.send(json.dumps(payload))