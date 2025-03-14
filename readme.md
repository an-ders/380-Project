use constants.py to test with 
`ENV = "TEST"`

# Structure

There are 5 main parts to the program.
1. drive forward on red line until target `drivetotarget.py`
2. pick up lego person `pickuplegoperson.py`
3. reverse until safezone in sight (INSERT FILE NAME)
4. drop off lego person (INSERT FILE NAME)
5. return to start point (INSERT FILE NAME, likely will reuse `drivetotarget.py` but make it flexible, with 2 modes)

## Other Files
`constants.py` holds constants
`img_processing.py` a module with some img related functions that are used by multiple other modules
`hardware.py` functions interacting directly with hardware
`wheel_calibration.py`
`colour_calibration.py`