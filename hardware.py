from constants import *
from test_classes import *
from gpiozero import Motor, RotaryEncoder
from time import time, sleep

ENV = "TEST"

right_motor = TestMotor(17, 27)  # GPIO 17 (Pin 11) -> Motor 1 Forward
left_motor = TestMotor(23, 24)  # GPIO 27 (Pin 13) -> Motor 1 Backward
# IN1 = TestDevice(17)  # GPIO 17 (Pin 11) -> Motor 1 Forward
# IN2 = TestDevice(27)  # GPIO 27 (Pin 13) -> Motor 1 Backward
# IN3 = TestDevice(23)  # GPIO 23 (Pin 16) -> Motor 2 Forward
# IN4 = TestDevice(24)  # GPIO 24 (Pin 18) -> Motor 2 Backward
# ENA = TestDevice(12)  # GPIO 12 (Pin 32) -> PWM for Motor A (PWM0)
# ENB = TestDevice(13)  # GPIO 13 (Pin 33) -> PWM for Motor B (PWM1)
encoder1 = TestEncoder(5, 6)
encoder2 = TestEncoder(16, 26)

if ENV != "TEST":
    right_motor = Motor(17, 27)  # GPIO 17 (Pin 11) -> Motor 1 Forward
    left_motor = Motor(23, 24)  # GPIO 27 (Pin 13) -> Motor 1 Backward
    left_encoder = RotaryEncoder(a = 5, b = 6, max_steps = 0)  # Encoder 1 (A=5, B=6)
    right_encoder = RotaryEncoder(a = 16, b = 26, max_steps = 0)  # Encoder 1 (A=16, B=26)

MAX_VOLTAGE = 12
MOTOR_VOLTAGE = 7
MAX_SPEED = MOTOR_VOLTAGE / MAX_VOLTAGE

WHEEL_D = 0.0677
WHEEL_CIRCUMFERENCE = 3.14159265359 * WHEEL_D

COUNTS_PER_REV = 14
GEAR_RATIO = 20.4
COUNTS_PER_OUT_REV = COUNTS_PER_REV * GEAR_RATIO

LEFT_MOTOR_STEPS_PER_REV = 263

RIGHT_MOTOR_FORWARD_STEPS_PER_REV = 240
RIGHT_MOTOR_BACKWARDS_STEPS_PER_REV = 220


# -------- DRIVE TRAIN -----------
# Function to calculate speed for Motor 1


def right_motor_speed():
    global last_time1
    global last_count1
    
    if last_time1 == None:
        last_time1 = time()
        return
    current_time = time()
    current_count = right_encoder.steps

    # Calculate speed
    delta_time = current_time - last_time1
    delta_count = current_count - last_count1
    if delta_time > 0:
        revolutions = delta_count / COUNTS_PER_OUT_REV
        distance = revolutions * WHEEL_CIRCUMFERENCE
        speed = distance / delta_time
    else:
        speed = 0

    # Update last time and last count
    last_time1 = current_time
    last_count1 = current_count

    return speed

# Function to calculate speed for Motor 2


def left_motor_speed():
    global last_time2
    global last_count2
    
    if last_time2 == None:
        last_time2 = time()
        return
    current_time = time()
    current_count = left_encoder.steps

    # Calculate speed
    delta_time = current_time - last_time2
    delta_count = current_count - last_count2
    if delta_time > 0:
        revolutions = delta_count / COUNTS_PER_OUT_REV
        distance = revolutions * WHEEL_CIRCUMFERENCE
        speed = distance / delta_time
    else:
        speed = 0

    # Update last time and last count
    last_time2 = current_time
    last_count2 = current_count

    return speed

# Function to calculate distance for Motor 1


def right_motor_distance():
    global total_distance1
    current_count = right_encoder.steps
    revolutions = current_count / 230
    total_distance1 = revolutions * WHEEL_CIRCUMFERENCE
    return total_distance1

# Function to calculate distance for Motor 2


def left_motor_distance():
    global total_distance2
    current_count = left_encoder.steps
    revolutions = current_count / 263
    total_distance2 = revolutions * WHEEL_CIRCUMFERENCE
    return total_distance2

# Function to calculate rotation in degrees for Motor 1


def right_motor_rotation():
    current_count = right_encoder.steps
    rotation_degrees = (current_count / 230) * 360
    return rotation_degrees

# Function to calculate rotation in degrees for Motor 2


def left_motor_rotation():
    current_count = left_encoder.steps
    rotation_degrees = (current_count / COUNTS_PER_OUT_REV) * 360
    return rotation_degrees


def drive_motors(left_speed, right_speed):
    drive_left_motor(left_speed)
    drive_right_motor(right_speed)


def stop_motors():
    left_motor.stop()
    right_motor.stop()


def turn(angle):
    return


def drive_right_motor(speed):
    if abs(speed) > MAX_SPEED:
        speed = MAX_SPEED
        
    speed = speed

    if speed == 0:
        right_motor.stop()
    elif speed < 0:
        right_motor.backward(speed=speed)
    else:
        right_motor.forward(speed=speed)


def drive_left_motor(speed):
    if abs(speed) > MAX_SPEED:
        speed = MAX_SPEED

    if speed == 0:
        left_motor.stop()
    elif speed < 0:
        left_motor.backward(speed=speed)
    else:
        left_motor.forward(speed=speed)

def lower_arm():  # TODO by Shreya
    return


def raise_arm():  # TODO by Shreya
    return

def map_speed_to_value(speed):
    # Input range
    speed_min = 0.3
    speed_max = 0.55
    
    # Output range
    value_min = 0.97
    value_max = 1.1
    
    # Linear mapping formula: y = mx + b
    # where m = (y2-y1)/(x2-x1)
    mapped_value = (value_max - value_min) * (speed - speed_min) / (speed_max - speed_min) + value_min
    
    # Clamp the output to the desired range
    return max(value_min, min(value_max, mapped_value))


# ------ TEST SCRIPT ------------
test_speed = 0.5
test_distance = 2

# if ENV != "TEST":
#     try:
#         while True:
#             drive_motors(test_speed, test_speed * 1.01)
# 
#             # Get encoder data for Motor 1
#             speed1 = 0
#             right_distance = right_motor_distance()
#             right_rotation = 0
#             print(
#                 f"Motor 1: Speed = {speed1:.2f} m/s, Distance = {right_distance:.2f} m, Rotation = {right_rotation:.2f}ÃÂ°")
# 
#             # Get encoder data for Motor 2
#             speed2 = 0
#             left_distance = left_motor_distance()
#             left_rotation = 0
#             print(
#                 f"Motor 2: Speed = {speed2:.2f} m/s, Distance = {left_distance:.2f} m, Rotation = {left_rotation:.2f}ÃÂ°")
# 
#             #stop_motors()
#             #sleep(2)
#             if abs(left_distance) >= test_distance or abs(right_distance) >= test_distance:
#                 break
# 
#     except KeyboardInterrupt:
#         print("Program stopped")
# 
#     finally:
#         stop_motors()
        
        
# try:
#     while True:
# #         print("Moving A forward")
# #         motors_forward(0.5)
# #         sleep(2)
# 
#         print("Moving Both forward")
#         drive_motors(0.25)
#         sleep(2)
#         
#         print("Stopping")
#         stop_motors()
#         sleep(2)
# 
# except KeyboardInterrupt:
#     print("Program stopped")
# 
# finally:
#     motorA_stop()
#     motorB_stop()
#     IN1.close()
#     IN2.close()
#     IN3.close()
#     IN4.close()
#     ENA.close()
#     ENB.close()


