# Set up detectors (adjust this list based on your specific needs)
detectors(['scaler', 'xrf', 'medipix'])

# Define the scan parameters
motor1 = samy  # Outer loop motor (slow axis)
startpos1 = 0
endpos1 = 100
numpts1 = 101

motor2 = samx  # Inner loop motor (fast axis)
startpos2 = 0
endpos2 = 100
numpts2 = 101

dettime = 0.01  # Exposure time in seconds

# Execute the 2D fly scan
fly2d(motor1, startpos1, endpos1, numpts1, motor2, startpos2, endpos2, numpts2, dettime, absolute=False)