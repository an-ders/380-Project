import numpy as np

import sys
sys.path.append('..')
from hardware import *

MIN_SPEED = 0.25
MAX_TEST_SPEED = MAX_SPEED * 0.7
STEP_SIZE = (MAX_TEST_SPEED - MIN_SPEED) / 5

print(MAX_TEST_SPEED)

def adjust_speed_right(speed):
    multiplier = 0.14 * speed + 0.937
    speed *= multiplier
    return speed

speed = MIN_SPEED
while speed <= MAX_TEST_SPEED + 0.01:
    print(speed)

    drive_motors(adjust_speed_right(speed), speed)
    while ((right_motor_distance() > -1.5) and (left_motor_distance() > -1.5)):
        continue;
    
    drive_motors(-adjust_speed_right(speed), -speed)
    while ((right_motor_distance() < 0) and (left_motor_distance() < 0)):
        continue;
    
    speed += STEP_SIZE