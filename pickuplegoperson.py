import img_processing as imgp
from constants import BLUE_HSV_RANGE
from hardware import *
from time import sleep

def get_center(x_min, x_max, y_min, y_max):
    # TODO by Zara
    # probably uses img_processing.get_midpoint
    return (center_x, center_y)

def get_color_location(img, color):
    """Gets min and max x and y coordinates of a color block"""
    # TODO consider moving to img_processing, but its likely not used anywhere else
    # TODO by Zara
    return x_min, x_max, y_min, y_max

def get_current_location(img):
    return (curr_x, curr_y)

def pick_up_lego_person_main():
    # TODO consider implementing feedback loop to ensure accurate control in this most critical and sensitive part of the program
    img = imgp.read_camera() # TODO GET RID OF THIS
    x_min, x_max, y_min, y_max = get_color_location(img, BLUE_HSV_RANGE)
    target_center = get_center(x_min, x_max, y_min, y_max)
    curr_loc = get_current_location(img)  # TODO this should probably just be a constant
    dist = imgp.get_length(curr_loc,target_center)
    drive_motors(dist)  # TODO maybe consider differential speed, or just some method to ensure we are driving straight to the center. might need to do offset calculation but with the target.
    sleep(SLEEP_TIME)
    lower_arm()
    sleep(SLEEP_TIME)
    raise_arm()
