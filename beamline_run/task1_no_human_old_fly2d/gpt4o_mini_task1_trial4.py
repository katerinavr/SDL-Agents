# filename: scan_100um_area.py
import epics
import time

# Define motors
fomx = epics.Motor('26idcnpi:m10.')  # Motor for x direction
fomy = epics.Motor('26idcnpi:m11.')  # Motor for y direction

# Scan parameters
start_x = -50.0  # Start position in micrometers
end_x = 50.0     # End position in micrometers
num_pts_x = 101  # Number of points (100 micrometers / 1 micrometer resolution + 1)
start_y = -50.0  # Start position in micrometers
end_y = 50.0     # End position in micrometers
num_pts_y = 101  # Number of points (100 micrometers / 1 micrometer resolution + 1)
det_time = 0.01  # Exposure time in seconds

# Execute the scan
fly2d(fomx, start_x, end_x, num_pts_x, fomy, start_y, end_y, num_pts_y, det_time)