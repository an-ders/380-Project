"""Module for part 1 of the program. Robot starts following the red line towards the target."""

from hardware.hardware import *
import img_processing as imgp
from math import log

MAX_TURNS = 9

# TODO CALIBRATE ME (BELOW)
MIN_LEN = 60  # cm
A = 1
B = 0
C = 0

# TODO TUNE ME - ZARA
def get_optimal_speed(line_len):
    speed = A*log(line_len + B) + C
    return speed

def get_line_len(img):
    # TODO READ LINES FROM IMAGE FIRST - ZARA
    x1_1, y1_1, x2_1, y2_1 = first_line
    x1_2, y1_2, x2_2, y2_2 = second_line
    midpoint_1 = imgp.get_midpoint((x1_1, y1_1), (x1_2, y1_2))
    midpoint_2 = imgp.get_midpoint((x2_1, y2_1), (x2_2, y2_2))
    line_len = imgp.get_length(midpoint_1, midpoint_2)
    return line_len

def drive_to_target_main(img):
    total_turns = 0
    while total_turns < MAX_TURNS:
        line_len = get_line_len(img)
        if line_len < MIN_LEN:
            # TODO 90 degree turn program
            total_turns += 1
        else:
            speed = get_optimal_speed(line_len)
            offset = get_offset(img)  # TODO by Anders
            left_speed, right_speed = get_differential_speed(offset, speed)  # TODO by Anders
            # TODO calibrate motors here
            drive_motors(left_speed, right_speed)
    # go to part 2