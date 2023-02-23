import pygame 
import lcm
import numpy as np
from lcmtypes import mbot_motor_command_t, timestamp_t
import time
import sys
import cv2

def main():
    lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")

    # initialization
    pygame.init()
    pygame.display.set_caption("MBot TeleOp")
    screen = pygame.display.set_mode([200,200])
    font = pygame.font.Font('freesansbold.ttf', 32)
    smaller_font = pygame.font.Font('freesansbold.ttf', 12)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    screen2 = pygame.display.set_mode([640,480])

    time.sleep(0.5)
    cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        ret, frame = cap.read()
        screen2.fill([0,0,0])
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = image.swapaxes(0,1)
        image = cv2.flip(image, -1)
        image = pygame.surfarray.make_surface(image)
        screen2.blit(image, (0,0))
        key_input = pygame.key.get_pressed() 
        cur_motor_command = mbot_motor_command_t()
        cur_motor_command.trans_v = 0.0
        cur_motor_command.angular_v = 0.0
        # screen.fill(white)
        if key_input[pygame.K_q]:
            pygame.quit()
            sys.exit()
        if key_input[pygame.K_LEFT]:
            text = font.render('LEFT', True, green, blue)
            cur_motor_command.angular_v = 2.0
        elif key_input[pygame.K_RIGHT]:
            text = font.render('RIGHT', True, green, blue)
            cur_motor_command.angular_v = -2.0
        if key_input[pygame.K_UP]:
            text = font.render('FORWARD', True, green, blue)
            cur_motor_command.trans_v = 0.25 # m/s
        elif key_input[pygame.K_DOWN]:
            text = font.render('BACKWARD', True, green, blue)
            cur_motor_command.trans_v = -0.25 # m/s
        if (cur_motor_command.trans_v == 0.0 and cur_motor_command.angular_v == 0.0):
            text = font.render('STOPPED', True, red, blue)
            text2 = smaller_font.render('arrow keys to drive | q to quit', True, red, blue)
            textRect2 = text2.get_rect()
            textRect2.center = (100, 150)
            # screen.blit(text2, textRect2)

        # add timestamp
        current_time = int(time.time() * 1e6)
        cur_motor_command.utime = current_time

        # add timesync message
        drive_time = timestamp_t()
        drive_time.utime = cur_motor_command.utime

        # publish messages
        lc.publish("MBOT_TIMESYNC", drive_time.encode())
        lc.publish("MBOT_MOTOR_COMMAND", cur_motor_command.encode())
        time.sleep(0.05)
        
        textRect = text.get_rect()
        textRect.center = (100, 100)
        screen.blit(text, textRect)
        pygame.display.update()

if __name__== "__main__":
    main()

