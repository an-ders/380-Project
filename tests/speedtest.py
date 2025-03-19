from hardware import *

MIN_SPEED = 0.25
MAX_TEST_SPEED = MAX_SPEED*0.7
STEP_SIZE = (MAX_TEST_SPEED-MAX_SPEED)/5

def adjust_speed_right(speed):
    multiplier = 0.14*speed + 0.937
    speed *= multiplier
    return speed


if __name__ == "__main__":
    for sp in range(MIN_SPEED, MAX_TEST_SPEED, STEP_SIZE):
        print(sp)
        while ((right_motor_distance()<1.5) and (left_motor_distance<1.5)):
           drive_motors(sp, adjust_speed_right(sp))