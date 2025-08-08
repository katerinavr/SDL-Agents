# Recommended measurement point (bright diffracting + isolated)

# • Coordinate:  zpx = –43 µm,   zpy = +46 µm   (±1 µm)
#   – It is the brightest spot in the nano-diffraction map.
#   – The same position is dark/low-intensity in the nano-fluorescence map, indicating that the particle is not part of a large (>10 µm) cluster and is likely an isolated grain of reasonable thickness.

# Action

# Please move the X-ray beam to (zpx, zpy) = (-43 µm, +46 µm) and center the scan there for the next measurement.

# filename: move_beam_to_isolated_particle.py
import sys, time
# Bring in the motion helper and piezo motors defined in S26_commandline.py
from S26_commandline import mov, zpx, zpy

# Target coordinates (µm) for the isolated, strongly-diffracting particle
TARGET_X = -43.0     # zpx  [µm]
TARGET_Y =  46.0     # zpy  [µm]

print(f"Current beam position →  zpx = {zpx.RBV:.2f} µm , zpy = {zpy.RBV:.2f} µm")

# Safety check – make sure the hybrid piezos are “locked”
if abs(zpx.RBV - zpx.VAL) > 100 or abs(zpy.RBV - zpy.VAL) > 100:
    print("ERROR: Hybrid piezos are >100 µm from their setpoint. "
          "Please run lock_hybrid() first, then re-execute this script.")
    sys.exit(1)

print(f"Moving beam to        →  zpx = {TARGET_X:.1f} µm , zpy = {TARGET_Y:.1f} µm")

# Perform the absolute moves
mov(zpx, TARGET_X)
mov(zpy, TARGET_Y)

time.sleep(1.0)   # allow motors to settle

print(f"Beam position after move →  zpx = {zpx.RBV:.2f} µm , zpy = {zpy.RBV:.2f} µm")
print("Beam centred on isolated, strongly-diffracting particle – ready for the next measurement.")
