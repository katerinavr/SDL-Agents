# filename: scan_area.py
import epics
import time

# Define parameters for the scan
motor1 = fomx  # X motor
motor2 = fomy  # Y motor
startpos1 = -50  # Start position for X motor
endpos1 = 50     # End position for X motor
numpts1 = 101    # Number of points in X direction
startpos2 = -50  # Start position for Y motor
endpos2 = 50     # End position for Y motor
numpts2 = 101    # Number of points in Y direction
dettime = 0.01   # Exposure time in seconds

# Execute the 2D scan
fly2d(motor1, startpos1, endpos1, numpts1, motor2, startpos2, endpos2, numpts2, dettime)