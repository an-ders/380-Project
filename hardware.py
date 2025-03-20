from test_classes import *
from gpiozero import Motor, RotaryEncoder, AngularServo
from time import time
import numpy as np

right_motor = Motor(17, 27)  # GPIO 17 (Pin 11) -> Motor 1 Forward  # GPIO 27 (Pin 13) -> Motor 1 Backward
left_motor = Motor(23, 24)  # GPIO 23 (Pin 16) -> Motor 2 Forward # GPIO 24 (Pin 18) -> Motor 2 Backward
left_encoder = RotaryEncoder(5, 6, max_steps=0)   #max_steps=0 allows us to look at raw steps # Encoder 1 (A=5, B=6)
right_encoder = RotaryEncoder(16, 26, max_steps=0)
servo = TestServo(22)  #servo = AngularServo(22, min_angle=0, max_angle=45)

FPS = 20

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

TURN_SPEED = 0.3

RED_HSV_RANGE = {
    'lower': np.array([0, 100, 130]),
    # THESE RED VALUES WORKED WELL FOR THE TRACK
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

# -------- DRIVE TRAIN -----------


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


def right_motor_distance():
    current_count = right_encoder.steps
    revolutions = current_count / 230
    return revolutions * WHEEL_CIRCUMFERENCE


def left_motor_distance():
    current_count = left_encoder.steps
    revolutions = current_count / 263
    return revolutions * WHEEL_CIRCUMFERENCE


def right_motor_rotation():
    current_count = right_encoder.steps
    rotation_degrees = (current_count / 230) * 360
    return rotation_degrees


def left_motor_rotation():
    current_count = left_encoder.steps
    rotation_degrees = (current_count / COUNTS_PER_OUT_REV) * 360
    return rotation_degrees


def drive_motors(left_speed, right_speed):
    drive_left_motor(left_speed)
    drive_right_motor(right_speed)
    

def drive_right_motor(speed):
    if abs(speed) > MAX_SPEED:
        speed = MAX_SPEED

    speed = speed

    if speed == 0:
        right_motor.stop()
    elif speed < 0:
        right_motor.backward(speed=abs(speed))
    else:
        right_motor.forward(speed=speed)


def drive_left_motor(speed):
    if abs(speed) > MAX_SPEED:
        speed = MAX_SPEED

    if speed == 0:
        left_motor.stop()
    elif speed < 0:
        left_motor.backward(speed=abs(speed))
    else:
        left_motor.forward(speed=speed)


def stop_motors():
    left_motor.stop()
    right_motor.stop()


def turn_right():
    left_steps = left_encoder.steps

    drive_motors(TURN_SPEED, 0)

    def get_distance1(steps):
        revolutions = steps / 263
        return revolutions * WHEEL_CIRCUMFERENCE

    while get_distance1(abs(left_encoder.steps - left_steps)) < 20:
        continue

    stop_motors()


def turn_left():
    right_steps = left_encoder.steps

    drive_motors(0, TURN_SPEED)

    def get_distance2(steps):
        revolutions = steps / 220
        return revolutions * WHEEL_CIRCUMFERENCE

    while get_distance2(abs(right_encoder.steps - right_steps)) < 20:
        continue

    stop_motors()


def lower_arm():
    servo.angle = 30


def raise_arm():
    servo.angle = 22


def drop_person():
    servo.angle = 10

