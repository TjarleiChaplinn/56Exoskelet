import pygame
import time
    
pygame.init()
pygame.joystick.init()
controller = pygame.joystick.Joystick(0)
controller.init()

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if controller.get_button(5):
                print("R1")
            elif controller.get_button(4):
                print("L1")
            elif controller.get_button(6):
                print("L2")
            elif controller.get_button(7):
                print("R2")