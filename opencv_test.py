import cv2
import json
import serial
import time
from simple_pid import PID

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

# Center turret
payload = {
    "laser": False,
    "pan":90,
    "tilt":90
}
turret.send(json.dumps(payload))

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cam_pan = 90
cam_tilt = 90
cap = cv2.VideoCapture(4)

def scale_coordinates(x, y):
    # Define the input range
    x_range = 640
    y_range = 480

    # Define the output range
    out_range = 180

    # Scale the X value
    scaled_x = (x / x_range) * out_range

    # Scale the Y value
    scaled_y = (y / y_range) * out_range

    return scaled_x, scaled_y

while True:
    ret, frame = cap.read()
    #Resize
    frame = cv2.resize(frame, (640, 480))

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(15, 15))
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Get center of face
        x_center = x + w // 2
        y_center = y + h // 2

        # Draw center of face
        cv2.circle(frame, (x_center, y_center), 2, (0, 0, 255), 2)

        cv2.rectangle(frame,(640//2-50,480//2-50),
                 (640//2+50,480//2+50),
                  (255,255,255),3)        
        
        # Move if face is not in center

        if x_center < 640//2-50:
            cam_pan -= 1
            laser = False
        elif x_center > 640//2+50:
            cam_pan += 1
            laser = False

        if y_center < 480//2-50:
            cam_tilt += 1
            laser = False
        elif y_center > 480//2+50:
            cam_tilt -= 1
            laser = False
        # if face in center
        if x_center > 640//2-50 and x_center < 640//2+50 and y_center > 480//2-50 and y_center < 480//2+50:
            print("Shoot")
            laser = True
        # Print the coordinates
        payload = {
            "laser": laser,
            "pan":int(cam_pan),
            "tilt":int(cam_tilt)
        }
        turret.send(json.dumps(payload))
    # Display the frame with bounding boxes
    cv2.imshow('Face Detection', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close the window
cap.release()
cv2.destroyAllWindows()