import numpy as np

FPS = 10
FRAME_WIDTH = 480
FRAME_HEIGHT = 480

# Robot Physical Constants
TRACK_WIDTH = 15       # cm - distance between wheels
WHEEL_DIAMETER = 6.5   # cm - diameter of wheels

# Wheel Calibration Constants
LEFT_WHEEL_OFFSET = 1
RIGHT_WHEEL_OFFSET = 1

# Camera Values
RED_HSV_RANGE = {
    'lower': np.array([0, 220, 220]), 
    'upper': np.array([60, 255, 255])
}
GREEN_HSV_RANGE = {
    'lower': np.array([40, 200, 40]),
    'upper': np.array([80, 255, 255])
}
BLUE_HSV_RANGE = {
    'lower': np.array([100, 100, 100]),
    'upper': np.array([130, 255, 255])
}
