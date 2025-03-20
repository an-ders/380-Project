import sys
sys.path.append('..')
from hardware import *

MIN_SPEED = 0.25
MAX_TEST_SPEED = MAX_SPEED*0.7
NUM_TESTS = 3
STEP_SIZE = (MAX_TEST_SPEED-MIN_SPEED)/NUM_TESTS
speed_list = [MIN_SPEED + i * STEP_SIZE for i in range(4)]  # 4 points including min and max

def adjust_speed_right(speed):
    multiplier = 0.14*speed + 0.937
    speed *= multiplier
    return speed


if __name__ == "__main__":
    speed_list = [MIN_SPEED + i * STEP_SIZE for i in range(NUM_TESTS+1)]
    for sp in speed_list:
        print(sp)
        drive_motors(sp, adjust_speed_right(sp))
        while (left_motor_distance<1.5):
           continue
        drive_motors(-sp, -adjust_speed_right(sp))
        while (left_motor_distance>0):
            continue