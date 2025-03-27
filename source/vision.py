import cv2 as cv
import numpy as np

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

RED_HSV_RANGE = {
    # Red hue range 1 (low end)
    'lower_red1' : np.array([0, 130, 130]),
    'upper_red1' : np.array([10, 255, 255]),

    # Red hue range 2 (high end)
    'lower_red2' : np.array([160, 100, 100]),
    'upper_red2' : np.array([180, 255, 255])
}
GREEN_HSV_RANGE = {
    'lower': np.array([40, 200, 40]),
    'upper': np.array([80, 255, 255])
}
BLUE_HSV_RANGE = {
    'lower': np.array([100, 100, 100]),
    'upper': np.array([130, 255, 255])
}

def getError(c):
    if c is None or len(c) == 0:  # Add check for empty contours
        return None
    try:
        x = centroid(c)
        if x == -1: 
            return None
        return (SCREEN_WIDTH // 2) - x
    except ValueError:  # Handle any other potential errors
        return None

def centroid(c):
    try:
        max_contour = max(c, key=cv.contourArea)
        mom = cv.moments(max_contour)

        if mom["m00"]:
            return int(mom["m10"] / mom["m00"])
    except ValueError:  # Handle case when no contours found
        return -1

    return -1