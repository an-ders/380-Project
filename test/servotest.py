import time as timer

import sys
sys.path.append('..')
from hardware import *

speed = 0.3

for i in range(20):
    print(f"Run {i}")
    drive_motors(speed, speed)
    timer.sleep(0.7)
    stop_motors()
    timer.sleep(2)

    lower_arm()
    timer.sleep(3)
    raise_arm()
    timer.sleep(3)

    drive_motors(-speed, -speed)
    timer.sleep(0.5)
    stop_motors()
    timer.sleep(2)

    drop_person()
    timer.sleep(2)

    drive_motors(-speed, -speed)
    timer.sleep(0.5)
    stop_motors()
    timer.sleep(2)