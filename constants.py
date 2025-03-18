import numpy as np

FPS = 30

# Robot Physical Constants
WHEEL_DIAMETER = 6.5   # cm - diameter of wheels

# Wheel Calibration Constants
LEFT_WHEEL_OFFSET = 1
RIGHT_WHEEL_OFFSET = 0.98

# Camera Values
RED_HSV_RANGE = {
    'lower': np.array([0, 100, 130]),
    'upper': np.array([90, 255, 255])

}
GREEN_HSV_RANGE = {
    'lower': np.array([40, 200, 40]),
    'upper': np.array([80, 255, 255])
}
BLUE_HSV_RANGE = {
    'lower': np.array([100, 100, 100]),
    'upper': np.array([130, 255, 255])
}

# RED_HSV_RANGE = {
#     'lower': np.array([50, 180, 200]),
#     'upper': np.array([190, 255, 255])
# }
# GREEN_HSV_RANGE = {
#     'lower': np.array([15, 70, 120]),
#     'upper': np.array([70, 255, 255])
# }
# BLUE_HSV_RANGE = {
#     'lower': np.array([50, 100, 140]),
#     'upper': np.array([120, 255, 255])
# }

# HSV Ranges for RED at crosshair:

# For use in code (RED):
# lower: np.array([6, 140, 219])
# upper: np.array([60, 255, 255])

# HSV Ranges for RED at crosshair:

# For use in code (RED):
# lower: np.array([8, 192, 207])
# upper: np.array([60, 255, 255])
