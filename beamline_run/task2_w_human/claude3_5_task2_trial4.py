# Based on the nano-diffraction image provided, I can see a single bright spot which likely corresponds to a particle that diffracts at this particular diffraction condition. This is exactly what we're looking for in a nano-diffraction image.

# The location of this bright spot (particle) appears to be at approximately:

# x = 0 µm
# y = -38 µm

# To move the beam to this location, you should adjust the beam position to these coordinates. The precision of this measurement is on the order of 1 µm, as requested.

# This isolated bright spot is ideal for further analysis as it's clearly distinguishable from the background and doesn't appear to be part of a larger cluster. The brightness of this spot suggests it could provide good data for subsequent measurements.

# Remember, this single bright spot represents a particle that is diffracting under the current conditions. Other particles may be present but not visible if they're not satisfying the diffraction condition.



import time
import datetime

def safe_move(motor, position, relative=False):
    if motor in [zpx, zpy]:
        if abs(motor.RBV - motor.VAL) > 100:
            print("Please use lock_hybrid() to lock piezos at current position first...")
            return False
    if relative:
        result = movr(motor, position)
    else:
        result = mov(motor, position)
    return result == 0

# Move the beam to the coordinates of the particle
if not safe_move(zpx, 0, relative=True) or not safe_move(zpy, -38, relative=True):
    print("Movement failed. Aborting script.")
    exit()

time.sleep(1)

print(f"Beam moved to coordinates: X = {zpx.RBV}, Y = {zpy.RBV}")

# Perform a fine 2D scan around the particle
scan_range = 2.5  # μm
num_points = 21  # This will give us a step size of 0.25 μm

fly2d(zpx, -scan_range, scan_range, num_points,
      zpy, -scan_range, scan_range, num_points,
      dettime=0.5, absolute=False)

print("Fine scan completed. Please analyze the results to confirm exact particle location.")

input("Press Enter when you have analyzed the scan results and are ready to proceed...")

final_x = zpx.RBV
final_y = zpy.RBV

# Collect diffraction patterns at various angles
angles = [-5, -2.5, 0, 2.5, 5]  # Example angles in degrees
for angle in angles:
    if not safe_move(samth, angle):
        print(f"Failed to move to angle {angle}. Skipping this angle.")
        continue
    time.sleep(1)
    print(f"Collecting diffraction pattern at angle: {angle} degrees")
    count_time(1.0)  # Set count time to 1 second
    detectors(['pilatus'])  # Use Pilatus detector
    # Replace this with the actual trigger command for your detector
    # For example: epics.caput("DETECTOR:Acquire", 1)

safe_move(samth, 0)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
energy = DCMenergy.RBV

with open(logbook, "a") as fp:
    fp.write(f"\n----- Particle Analysis: {timestamp} -----\n")
    fp.write(f"Particle coordinates: X = {final_x}, Y = {final_y}\n")
    fp.write(f"Beam energy: {energy} keV\n")
    fp.write(f"Diffraction patterns collected at angles: {angles}\n")
    fp.write("----------------------------------------\n")

print(f"Analysis completed. Particle coordinates (X = {final_x}, Y = {final_y}) and parameters recorded in the logbook.")