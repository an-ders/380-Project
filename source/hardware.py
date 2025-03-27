from .test_classes import *
from gpiozero import Motor, RotaryEncoder, AngularServo, BadPinFactory
from time import time, sleep

# Try/except block creates variables on the global scope and prevents errors from halting runtime
try:
    # GPIO 17 (Pin 11) -> Motor 1 Forward  # GPIO 27 (Pin 13) -> Motor 1 Backward
    right_motor = Motor(17, 27, enable=12)
    # GPIO 23 (Pin 16) -> Motor 2 Forward # GPIO 24 (Pin 18) -> Motor 2 Backward
    left_motor = Motor(23, 24, enable=13)
    # left_encoder = RotaryEncoder(5, 6, max_steps=0)   #max_steps=0 allows us to look at raw steps # Encoder 1 (A=5, B=6)
    # right_encoder = RotaryEncoder(16, 26, max_steps=0)
    # servo = AngularServo(22, min_angle=0, max_angle=45)
except BadPinFactory:
    print("Error: BadPinFactory. Mocking hardware.")
    # GPIO 17 (Pin 11) -> Motor 1 Forward  # GPIO 27 (Pin 13) -> Motor 1 Backward
    right_motor = TestMotor(17, 27)
    # GPIO 23 (Pin 16) -> Motor 2 Forward # GPIO 24 (Pin 18) -> Motor 2 Backward
    left_motor = TestMotor(23, 24)
    # left_encoder = TestEncoder(5, 6)   #max_steps=0 allows us to look at raw steps # Encoder 1 (A=5, B=6)
    # right_encoder = TestEncoder(16, 26)
    # servo = TestServo(22)

MAX_VOLTAGE = 12
MOTOR_VOLTAGE = 7
MAX_DUTY_CYCLE = MOTOR_VOLTAGE / MAX_VOLTAGE
MIN_DUTY_CYCLE = 0.19

WHEEL_D = 0.0677
WHEEL_CIRCUMFERENCE = 3.14159265359 * WHEEL_D

COUNTS_PER_REV = 14
GEAR_RATIO = 20.4
COUNTS_PER_OUT_REV = COUNTS_PER_REV * GEAR_RATIO

LEFT_MOTOR_STEPS_PER_REV = 263
RIGHT_MOTOR_FORWARD_STEPS_PER_REV = 230

# -------- DRIVE TRAIN -----------

def drive_motors(left_speed, right_speed):
    drive_left_motor(left_speed)
    drive_right_motor(right_speed)


def drive_right_motor(speed):
    if abs(speed) > MAX_DUTY_CYCLE:
        speed = MAX_DUTY_CYCLE

    speed = speed

    if speed == 0:
        right_motor.stop()
    elif speed < 0:
        right_motor.backward(speed=abs(speed))
    else:
        right_motor.forward(speed=speed)


def drive_left_motor(speed):
    if abs(speed) > MAX_DUTY_CYCLE:
        speed = MAX_DUTY_CYCLE

    if speed == 0:
        left_motor.stop()
    elif speed < 0:
        left_motor.backward(speed=abs(speed))
    else:
        left_motor.forward(speed=speed)


def stop_motors():
    left_motor.stop()
    right_motor.stop()


if __name__ == "__main__":
    try:
        print("Testing motors.")

        print("Right motor forwards.")
        drive_right_motor(MIN_DUTY_CYCLE)
        sleep(1)
        print("Right motor backwards.")
        drive_right_motor(-MIN_DUTY_CYCLE)
        sleep(1)
        drive_right_motor(0)

        print("Left motor forwards.")
        drive_left_motor(MIN_DUTY_CYCLE)
        sleep(1)
        print("Left motor backwards.")
        drive_left_motor(-MIN_DUTY_CYCLE)
        sleep(1)
        drive_left_motor(0)

        print("Both motors forwards.")
        drive_motors(MIN_DUTY_CYCLE, MIN_DUTY_CYCLE)
        sleep(1)
        print("Both motors backwards.")
        drive_motors(-MIN_DUTY_CYCLE, -MIN_DUTY_CYCLE)
        sleep(1)
        stop_motors()

    except:
        stop_motors()
        raise


# def right_motor_speed():
#     global last_time1
#     global last_count1

#     if last_time1 == None:
#         last_time1 = time()
#         return
#     current_time = time()
#     current_count = right_encoder.steps

#     # Calculate speed
#     delta_time = current_time - last_time1
#     delta_count = current_count - last_count1
#     if delta_time > 0:
#         revolutions = delta_count / COUNTS_PER_OUT_REV
#         distance = revolutions * WHEEL_CIRCUMFERENCE
#         speed = distance / delta_time
#     else:
#         speed = 0

#     # Update last time and last count
#     last_time1 = current_time
#     last_count1 = current_count

#     return speed


# def left_motor_speed():
#     global last_time2
#     global last_count2

#     if last_time2 == None:
#         last_time2 = time()
#         return
#     current_time = time()
#     current_count = left_encoder.steps

#     # Calculate speed
#     delta_time = current_time - last_time2
#     delta_count = current_count - last_count2
#     if delta_time > 0:
#         revolutions = delta_count / COUNTS_PER_OUT_REV
#         distance = revolutions * WHEEL_CIRCUMFERENCE
#         speed = distance / delta_time
#     else:
#         speed = 0

#     # Update last time and last count
#     last_time2 = current_time
#     last_count2 = current_count

#     return speed


# def right_motor_distance():
#     current_count = right_encoder.steps
#     revolutions = current_count / 230
#     # Forward gives negative values so must *-1
#     return -1*(revolutions * WHEEL_CIRCUMFERENCE)


# def left_motor_distance():
#     current_count = left_encoder.steps
#     revolutions = current_count / 263
#     return revolutions * WHEEL_CIRCUMFERENCE


# def right_motor_rotation():
#     current_count = right_encoder.steps
#     rotation_degrees = (current_count / 230) * 360
#     return rotation_degrees


# def left_motor_rotation():
#     current_count = left_encoder.steps
#     rotation_degrees = (current_count / COUNTS_PER_OUT_REV) * 360
#     return rotation_degrees




# def right_motor_speed():
#     global last_time1
#     global last_count1

#     if last_time1 == None:
#         last_time1 = time()
#         return
#     current_time = time()
#     current_count = right_encoder.steps

#     # Calculate speed
#     delta_time = current_time - last_time1
#     delta_count = current_count - last_count1
#     if delta_time > 0:
#         revolutions = delta_count / COUNTS_PER_OUT_REV
#         distance = revolutions * WHEEL_CIRCUMFERENCE
#         speed = distance / delta_time
#     else:
#         speed = 0

#     # Update last time and last count
#     last_time1 = current_time
#     last_count1 = current_count

#     return speed


# def left_motor_speed():
#     global last_time2
#     global last_count2

#     if last_time2 == None:
#         last_time2 = time()
#         return
#     current_time = time()
#     current_count = left_encoder.steps

#     # Calculate speed
#     delta_time = current_time - last_time2
#     delta_count = current_count - last_count2
#     if delta_time > 0:
#         revolutions = delta_count / COUNTS_PER_OUT_REV
#         distance = revolutions * WHEEL_CIRCUMFERENCE
#         speed = distance / delta_time
#     else:
#         speed = 0

#     # Update last time and last count
#     last_time2 = current_time
#     last_count2 = current_count

#     return speed


# def right_motor_distance():
#     current_count = right_encoder.steps
#     revolutions = current_count / 230
#     # Forward gives negative values so must *-1
#     return -1*(revolutions * WHEEL_CIRCUMFERENCE)


# def left_motor_distance():
#     current_count = left_encoder.steps
#     revolutions = current_count / 263
#     return revolutions * WHEEL_CIRCUMFERENCE


# def right_motor_rotation():
#     current_count = right_encoder.steps
#     rotation_degrees = (current_count / 230) * 360
#     return rotation_degrees


# def left_motor_rotation():
#     current_count = left_encoder.steps
#     rotation_degrees = (current_count / COUNTS_PER_OUT_REV) * 360
#     return rotation_degrees


# def turn_right():
#     left_steps = left_encoder.steps

#     drive_motors(TURN_SPEED, 0)

#     def get_distance1(steps):
#         revolutions = steps / 263
#         return revolutions * WHEEL_CIRCUMFERENCE

#     while get_distance1(abs(left_encoder.steps - left_steps)) < 20:
#         continue

#     stop_motors()

# def turn_left2():
#     drive_motors(0, MIN_DUTY_CYCLE)
#     while right_motor_distance()<TURN_DIST:
#         print(right_motor_distance())
#     stop_motors()

# def turn_right2():
#     drive_motors(MIN_DUTY_CYCLE, 0)
#     while left_motor_distance()<TURN_DIST:
#         print(left_motor_distance())
#     stop_motors()

# def turn_left():
#     right_steps = left_encoder.steps

#     drive_motors(0, TURN_SPEED)

#     def get_distance2(steps):
#         revolutions = steps / 220
#         return revolutions * WHEEL_CIRCUMFERENCE

#     while get_distance2(abs(right_encoder.steps - right_steps)) < 20:
#         continue

#     stop_motors()


# def lower_arm():
#     servo.angle = 40


# def raise_arm():
#     servo.angle = 30
# def drop_person():
#     servo.angle = 0
