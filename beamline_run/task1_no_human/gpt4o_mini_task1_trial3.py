# filename: scan_100um_area.py
import epics
import time
import numpy as np  # Import numpy for calculations

# Define motors
fomx = epics.Motor('26idcnpi:m10.')  # Motor for x direction
fomy = epics.Motor('26idcnpi:m11.')  # Motor for y direction

# Scan parameters
startpos_x = -50.0  # Start position for x (in um)
endpos_x = 50.0     # End position for x (in um)
startpos_y = -50.0  # Start position for y (in um)
endpos_y = 50.0     # End position for y (in um)
numpts_x = int((endpos_x - startpos_x) / 1.0) + 1  # Number of points in x direction
numpts_y = int((endpos_y - startpos_y) / 1.0) + 1  # Number of points in y direction
dettime = 0.01      # Exposure time in seconds

# Execute the scan
try:
    fly2d(fomx, startpos_x, endpos_x, numpts_x, fomy, startpos_y, endpos_y, numpts_y, dettime)
    print("Scan completed successfully.")
except Exception as e:
    print(f"An error occurred during the scan: {e}")