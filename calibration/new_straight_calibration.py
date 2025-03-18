import numpy as np

def straight_calibration():
    # Constants
    TRACK_WIDTH = 16.25  # cm - distance between wheels
    TARGET_DISTANCE = 120  # cm - target straight line distance
    WHEEL_DIAMETER = 6.67
    
    print(f"\nStraight Line Calibration")
    print(f"-------------------------")
    print(f"Please drive the robot forward {TARGET_DISTANCE} cm")
    input("Press Enter when ready to begin...")
    
    # Get measurements
    lateral_offset = float(input("Enter lateral offset from straight line (cm, + for right, - for left): "))
    
    # Calculate actual distance traveled using Pythagorean theorem
    actual_distance = np.sqrt(TARGET_DISTANCE**2 + lateral_offset**2)
    
    # Calculate arc length for each wheel
    # For a curved path, outer wheel travels further than inner wheel
    # Using the arc length formula: length = radius * angle
    # Where angle = 2 * arcsin(chord_length / (2 * radius))
    
    if lateral_offset != 0:
        # Calculate radius of turn to center point
        radius = (TARGET_DISTANCE**2 + lateral_offset**2) / (2 * abs(lateral_offset))
        
        # Calculate outer and inner wheel radii
        if lateral_offset > 0:  # Drifted right
            outer_radius = radius + (TRACK_WIDTH/2)
            inner_radius = radius - (TRACK_WIDTH/2)
            # Right wheel traveled further (outer)
            right_distance = outer_radius * 2 * np.arcsin(actual_distance/(2*radius))
            left_distance = inner_radius * 2 * np.arcsin(actual_distance/(2*radius))
        else:  # Drifted left
            outer_radius = radius + (TRACK_WIDTH/2)
            inner_radius = radius - (TRACK_WIDTH/2)
            # Left wheel traveled further (outer)
            left_distance = outer_radius * 2 * np.arcsin(actual_distance/(2*radius))
            right_distance = inner_radius * 2 * np.arcsin(actual_distance/(2*radius))
            
        # Calculate multipliers based on distance ratio
        # The wheel that traveled further needs to be slowed down
        if left_distance > right_distance:
            left_multiplier = right_distance/left_distance
            right_multiplier = 1.0
        else:
            right_multiplier = left_distance/right_distance
            left_multiplier = 1.0
    else:
        # If no lateral offset, keep multipliers at 1.0
        left_multiplier = 1.0
        right_multiplier = 1.0
        
    print(f"\nResults:")
    print(f"Calculated actual distance: {actual_distance:.1f} cm")
    print(f"Calculated wheel distances:")
    print(f"Left wheel: {left_distance:.1f} cm")
    print(f"Right wheel: {right_distance:.1f} cm")
    print(f"\nSpeed multipliers:")
    print(f"Left wheel: {left_multiplier:.3f}")
    print(f"Right wheel: {right_multiplier:.3f}")
    
    return left_multiplier, right_multiplier

if __name__ == "__main__":
    straight_calibration()

