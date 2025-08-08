# filename: scan_100um_area.py
import epics
import time

# Ensure motors for moving the x-ray beam are defined
motor_x = zpx  # Motor for moving the x-ray beam in the x direction
motor_y = zpy  # Motor for moving the x-ray beam in the y direction

# Define parameters for the scan
start_x = -50.0  # Start position in micrometers (half of 100 micrometers)
end_x = 50.0     # End position in micrometers
start_y = -50.0  # Start position in micrometers
end_y = 50.0     # End position in micrometers
resolution = 1.0  # Resolution in micrometers
det_time = 0.01  # Exposure time in seconds

# Calculate number of points
num_pts_x = int((end_x - start_x) / resolution) + 1
num_pts_y = int((end_y - start_y) / resolution) + 1

# Log the scan parameters
logbook = "scan_log.txt"  # Define logbook file
try:
    with open(logbook, "a") as fp:
        fp.write(f'Starting scan: {num_pts_x} points in x, {num_pts_y} points in y, exposure time: {det_time} seconds\n')
except Exception as e:
    print(f"Error opening logbook: {e}")

# Execute the scan
try:
    fly2d(motor_x, start_x, end_x, num_pts_x, motor_y, start_y, end_y, num_pts_y, det_time)
except Exception as e:
    print(f"Error during scan execution: {e}")