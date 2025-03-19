"""Module of image processing functions used across multiple modules."""
import cv2 as cv
from constants import *

def get_midpoint(p1, p2):
    return (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
    
def get_length(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**(1/2)

    # center_x, center_y = get_center(x_min, x_max, y_min, y_max)
    # dist = get_distance_to_point(center_x, center_y)