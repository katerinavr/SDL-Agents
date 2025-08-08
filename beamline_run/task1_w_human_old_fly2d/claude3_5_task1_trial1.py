import time
import numpy as np

# First, let's set up the detectors
detectors(['scaler', 'xrf'])  # Adjust this list based on which detectors you want to use

# Set up scan parameters
motor1 = zpx  # X-axis motor
motor2 = zpy  # Y-axis motor
startpos1 = -50  # Start position for X-axis (micrometers)
endpos1 = 50     # End position for X-axis (micrometers)
numpts1 = 101    # Number of points in X-axis (100 steps + 1 for the start point)
startpos2 = -50  # Start position for Y-axis (micrometers)
endpos2 = 50     # End position for Y-axis (micrometers)
numpts2 = 101    # Number of points in Y-axis (100 steps + 1 for the start point)
dettime = 0.01   # Exposure time (seconds)

# Check if piezos are locked
if abs(zpx.RBV - zpx.VAL) > 100 or abs(zpy.RBV - zpy.VAL) > 100:
    print("Piezos are not locked. Attempting to lock piezos now...")
    try:
        lock_hybrid()
        time.sleep(1)  # Wait for locking to complete
        print("Piezos locked successfully.")
    except Exception as e:
        print(f"Error occurred while locking piezos: {e}")
        print("Please lock piezos manually before proceeding.")

# Check if current position allows for full range of motion
current_x = zpx.RBV
current_y = zpy.RBV
if abs(current_x) > 10 or abs(current_y) > 10:
    print("Warning: Current zone plate position may not allow for full range of motion.")
    print(f"Current position: X = {current_x}, Y = {current_y}")
    print("Consider centering the zone plate before scanning.")
    center = input("Do you want to center the zone plate now? (y/n): ")
    if center.lower() == 'y':
        zpx.move(0)
        zpy.move(0)
        time.sleep(2)  # Wait for movement to complete
        print("Zone plate centered.")

# Inform about scan time and offer segmentation option
total_points = numpts1 * numpts2
estimated_time = total_points * dettime
print(f"This scan will take approximately {estimated_time:.2f} seconds (excluding motor movement time).")

segment = input("Do you want to segment the scan for better beam stability? (y/n): ")
if segment.lower() == 'y':
    num_segments = int(input("Enter the number of segments: "))
    segment_size = numpts2 // num_segments
    print(f"The scan will be divided into {num_segments} segments of {segment_size} lines each.")

# Confirm to proceed
proceed = input("Do you want to proceed with the scan? (y/n): ")
if proceed.lower() != 'y':
    print("Scan aborted.")
else:
    if segment.lower() == 'y':
        for i in range(num_segments):
            start = i * segment_size
            end = (i + 1) * segment_size if i < num_segments - 1 else numpts2
            print(f"Scanning segment {i+1}/{num_segments}...")
            fly2d(motor1, startpos1, endpos1, numpts1, motor2,
                  startpos2 + (start/numpts2)*(endpos2-startpos2),
                  startpos2 + (end/numpts2)*(endpos2-startpos2),
                  end - start, dettime)
            time.sleep(1)  # Short pause between segments
    else:
        # Execute the fly2d function
        fly2d(motor1, startpos1, endpos1, numpts1, motor2, startpos2, endpos2, numpts2, dettime)

    print("Scan completed. Please check the saved data to ensure it was collected properly.")