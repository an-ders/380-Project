"""Module of image processing functions used across multiple modules."""
import cv2 as cv
from constants import *

def read_camera():
    # Initialize webcam
    cap = cv.VideoCapture(0)

    # Set video parameters
    native_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    native_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # Set video parameters
    cap.set(cv.CAP_PROP_FRAME_WIDTH, native_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, native_height)
    cap.set(cv.CAP_PROP_FPS, FPS)

    # Phase 1: Wait for red line detection
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
    return frame

def get_midpoint(p1, p2):
    return (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
    
def get_length(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**(1/2)

    center_x, center_y = get_center(x_min, x_max, y_min, y_max)
    dist = get_distance_to_point(center_x, center_y)