import numpy as np

def wheel_calibration():
    # Constants
    TARGET_DISTANCE = 120  # cm - distance to drive
    TRACK_WIDTH = 16.25       # cm - distance between wheels

    
    print("Drive the robot forward", TARGET_DISTANCE, "cm")
    input("Press Enter after robot has completed driving...")
    
    # Get deviation measurement
    deviation = float(input("Enter deviation from straight line in cm (+ for right deviation, - for left): "))
    
    if deviation == 0:
        print("Robot drove straight, no adjustment needed")
        
    # Calculate arc length robot actually drove
    # Using deviation as height of circular segment
    # Arc length ≈ sqrt(4h² + c²) where h is deviation and c is chord length (TARGET_DISTANCE)
    actual_distance = np.sqrt(4 * deviation**2 + TARGET_DISTANCE**2)
    
    # Calculate radius of turn
    # R = (L/2) / sin(θ/2) where L is chord length and θ is central angle
    # θ = 2 * arcsin(deviation / R)
    # Solving for R:
    turn_radius = (TARGET_DISTANCE**2 + 4*deviation**2) / (8 * abs(deviation))
    
    # Calculate wheel speeds needed for this turn radius
    # Inner wheel needs to go slower than outer wheel
    # Speed ratio = (R - track_width/2) / (R + track_width/2)
    
    speed_ratio = (turn_radius - TRACK_WIDTH/2) / (turn_radius + TRACK_WIDTH/2)
    
    print(speed_ratio)
        
    print(f"\nNew wheel offset factors:")
    print(f"Left wheel: {new_left_offset:.3f}")
    print(f"Right wheel: {new_right_offset:.3f}")

wheel_calibration()
