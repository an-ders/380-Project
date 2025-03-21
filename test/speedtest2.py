from time import time

import sys
sys.path.append('..')
from hardware import *

MIN_SPEED = 0.25
MAX_TEST_SPEED = MAX_SPEED*0.7
NUM_TESTS = 3
STEP_SIZE = (MAX_TEST_SPEED-MIN_SPEED)/NUM_TESTS
DIST = 1.5

def adjust_speed_right(speed):
    multiplier = 0.14*speed + 0.937
    speed *= multiplier
    return speed

if __name__ == "__main__":
    speed_list = [MIN_SPEED + i * STEP_SIZE for i in range(NUM_TESTS+1)]
    for sp in speed_list:
        print("Setting duty cycle to %.2f", sp)

        # FORWARD
        drive_motors(sp, sp)
        start_time = time()
        while (right_motor_distance()<DIST):
            continue
        end_time = time()
        print("Actual forward speed: %.2f m/s", DIST/(end_time-start_time))

        # BACKWARD
        drive_motors(-sp, -sp)
        start_time = time()
        while (right_motor_distance()>0):
            continue
        end_time = time()
        print("Actual backward speed: %.2f m/s", DIST/(end_time-start_time))

        # STOP
        drive_motors(0, 0)