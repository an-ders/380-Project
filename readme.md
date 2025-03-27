# Structure

There are 2 main parts to the program.
1. follow the line till you cant see any more red `follow_line.py`
2. pick up lego person and turn around (search for new line) `pickup.py`

`gameday.py` just uses the above functions to drive to the target then pickup/turn around, then drive back

## Other Files
`hardware.py` functions and constants relating to the hardware
`wheel_calibration.py`
`colour_calibration.py` used for taking real world HSV values
`test_valsses.py` used to mock hardware abstraction layer when running without hardware attached
`vision.py` functions and constants relating to the vision and processing the line
