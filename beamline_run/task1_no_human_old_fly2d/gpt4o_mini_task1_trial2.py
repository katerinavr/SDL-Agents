# filename: scan_100um_area.py
import epics
import time

# Ensure motors are defined
# Assuming these motors are already defined in the main script
# fomx = epics.Motor('26idcnpi:m10.')
# fomy = epics.Motor('26idcnpi:m11.')

# Define scan parameters
motor_x = fomx  # Motor for x direction
motor_y = fomy  # Motor for y direction
start_x = -50.0  # Start position in x (half of 100 um)
end_x = 50.0     # End position in x
start_y = -50.0  # Start position in y (half of 100 um)
end_y = 50.0     # End position in y
resolution = 1.0  # Resolution in um
det_time = 0.01  # Exposure time in seconds

# Calculate number of points
num_pts_x = int((end_x - start_x) / resolution) + 1
num_pts_y = int((end_y - start_y) / resolution) + 1

# Check if motors are ready (optional)
if motor_x.is_ready() and motor_y.is_ready():
    # Execute the scan
    fly2d(motor_x, start_x, end_x, num_pts_x, motor_y, start_y, end_y, num_pts_y, det_time)
else:
    print("One or both motors are not ready for movement.")