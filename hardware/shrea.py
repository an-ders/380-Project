from gpiozero import PWMOutputDevice, DigitalOutputDevice, RotaryEncoder
# from RotaryEncoder import steps
from time import time, sleep

IN1 = DigitalOutputDevice(17); # GPIO 17 (Pin 11) -> Motor 1 Forward
IN2 = DigitalOutputDevice(27); # GPIO 27 (Pin 13) -> Motor 1 Backward
IN3 = DigitalOutputDevice(23); # GPIO 23 (Pin 16) -> Motor 2 Forward
IN4 = DigitalOutputDevice(24); # GPIO 24 (Pin 18) -> Motor 2 Backward
ENA = PWMOutputDevice(12); # GPIO 12 (Pin 32) -> PWM for Motor A (PWM0)
ENB = PWMOutputDevice(13); # GPIO 13 (Pin 33) -> PWM for Motor B (PWM1)
encoder1 = RotaryEncoder(5,6) # Encoder 1 (A=5, B=6)
encoder2 = RotaryEncoder(16,26) # Encoder 1 (A=16, B=26)

WHEEL_D = 0.067
WHEEL_CIRCUMFERENCE = 3.14159 * WHEEL_D

COUNTS_PER_REV = 14
GEAR_RATIO = 20.4
COUNTS_PER_OUT_REV = COUNTS_PER_REV * GEAR_RATIO

last_time1 = time()
last_time2 = time()
last_count1 = 0
last_count2 = 0
total_distance1 = 0
total_distance2 = 0

max_voltage = 12
motor_voltage = 7
max_duty_cycle = motor_voltage / max_voltage

# Function to calculate speed for Motor 1
def get_speed1():
    global last_time1, last_count1
    current_time = time()
    current_count = encoder1.steps
    
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
def get_speed2():
    global last_time2, last_count2
    current_time = time()
    current_count = encoder2.steps
    
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
def get_distance1():
    global total_distance1
    current_count = encoder1.steps
    revolutions = current_count / COUNTS_PER_OUT_REV
    total_distance1 = revolutions * WHEEL_CIRCUMFERENCE
    return total_distance1

# Function to calculate distance for Motor 2
def get_distance2():
    global total_distance2
    current_count = encoder2.steps
    revolutions = current_count / COUNTS_PER_OUT_REV
    total_distance2 = revolutions * WHEEL_CIRCUMFERENCE
    return total_distance2

# Function to calculate rotation in degrees for Motor 1
def get_rotation1():
    current_count = encoder1.steps
    rotation_degrees = (current_count / COUNTS_PER_OUT_REV) * 360
    return rotation_degrees

# Function to calculate rotation in degrees for Motor 2
def get_rotation2():
    current_count = encoder2.steps
    rotation_degrees = (current_count / COUNTS_PER_OUT_REV) * 360
    return rotation_degrees

def motorA_forward(speed):
    if speed > max_duty_cycle:
        speed = max_duty_cycle
    IN1.on()
    IN2.off()
    ENA.value = speed

def motorA_backward(speed):
    if speed > max_duty_cycle:
        speed = max_duty_cycle
    IN1.off()
    IN2.on()
    ENA.value = speed

def motorB_forward(speed):
    if speed > max_duty_cycle:
        speed = max_duty_cycle
    IN3.on()
    IN4.off()
    ENB.value = speed
    
def motorB_backward(speed):
    if speed > max_duty_cycle:
        speed = max_duty_cycle
    IN3.off()
    IN4.on()
    ENB.value = speed

def motorA_stop():
    IN1.off()
    IN2.off()
    ENA.value = 0
    
def motorB_stop():
    IN3.off()
    IN4.off()
    ENB.value = 0

def motors_forward(speed):
    motorA_forward(speed);
    motorB_forward(speed);

def motors_backward(speed):
    motorA_backward(speed);
    motorB_backward(speed);

def turn_left(speed):
    motorA_backward(speed);
    motorB_forward(speed);

def turn_right(speed):
    motorA_forward(speed);
    motorB_backward(speed);
    
def motors_stop():
    motorA_stop()
    motorB_stop()

try:
    while True:
        print("Moving B forward")
        motors_forward(0.2)
        sleep(2)
        
        # Get encoder data for Motor 1
        speed1 = get_speed1()
        distance1 = get_distance1()
        rotation1 = get_rotation1()
        print(f"Motor 1: Speed = {speed1:.2f} m/s, Distance = {distance1:.2f} m, Rotation = {rotation1:.2f}Â°")
        
        # Get encoder data for Motor 2
        speed2 = get_speed2()
        distance2 = get_distance2()
        rotation2 = get_rotation2()
        print(f"Motor 2: Speed = {speed2:.2f} m/s, Distance = {distance2:.2f} m, Rotation = {rotation2:.2f}Â°")
        
        print("Stopping")
        motors_stop()
        sleep(2)


except KeyboardInterrupt:
    print("Program stopped")

finally:
    motorA_stop()
    motorB_stop()
    IN1.close()
    IN2.close()
    IN3.close()
    IN4.close()
    ENA.close()
    ENB.close()