import sys
sys.path.append('..')
from hardware import *

MIN_DUTY_CYCLE = 0.25
MAX_TEST_SPEED = MAX_DUTY_CYCLE*0.7
NUM_TESTS = 3
STEP_SIZE = (MAX_TEST_SPEED-MIN_DUTY_CYCLE)/NUM_TESTS

def adjust_speed_right(speed):
    multiplier = 0.14*speed + 0.937
    speed *= multiplier
    return speed

if __name__ == "__main__":
    speed_list = [MIN_DUTY_CYCLE + i * STEP_SIZE for i in range(NUM_TESTS+1)]
    for sp in speed_list:
        print(sp)
        drive_motors(sp, sp)
        while (right_motor_distance()<1):
            print(right_motor_distance())
        drive_motors(-sp, -sp)
        while (left_motor_distance()>0):
           print(left_motor_distance())
        drive_motors(0, 0)
