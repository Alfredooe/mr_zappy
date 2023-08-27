import pygame

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

# Initialize Pygame
pygame.init()

# Set the window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
pygame.mouse.set_cursor(*pygame.cursors.broken_x)
# Set the scale for the mouse coordinates
SCALE = 180
laser = False
font = pygame.font.Font(None, 30)
# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            laser = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            laser = False

    mouse_pos = pygame.mouse.get_pos()

    x = int((mouse_pos[0] / WINDOW_WIDTH) * SCALE)
    y = 180 - int((mouse_pos[1] / WINDOW_HEIGHT) * SCALE)
    text_surface = font.render(f"Mouse: ({x}, {y})", True, (255, 255, 255))

    #print(f"Mouse position: ({x}, {y})")

    screen.fill((255, 255, 255))
    screen.fill((0, 0, 0))
    
    screen.blit(text_surface, (10, 10))
    pygame.display.flip()

    payload = {
        "laser": laser,
        "pan":x,
        "tilt": y
    }
    print(payload)
    turret.send(json.dumps(payload))
    time.sleep(0.01)
pygame.quit()