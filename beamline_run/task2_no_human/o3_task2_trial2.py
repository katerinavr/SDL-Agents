# The diffracting particle is the intense yellow-green pixel located just below the centre of the bottom half of the scan.

# Estimated position (±1 µm):
# • zpx  ≈ 0 µm
# • zpy  ≈ –39 µm

# Please move the beam to (zpx, zpy) = (0 µm, –39 µm).

# filename: move_beam_to_particle.py
#
# Purpose: centre the x-ray beam on the diffracting particle found in the
#          previous scan  ➜  (zpx , zpy) = (0 µm , –39 µm)
#
# Safety notes
#   • Uses the approved `mov()` helper from S26_commandline.py
#   • Refuses to run if the requested jump exceeds ±50 µm unless the user
#     has first “locked” the piezos with lock_hybrid()

import time
from S26_commandline import mov, zpx, zpy   # sanctioned motion helpers

# ----------------------------------------------------------------------
# user-defined target (µm)
TARGET_ZPX = 0.0
TARGET_ZPY = -39.0
# ----------------------------------------------------------------------

# Safety check – make sure the requested step is within the 50 µm rule
if abs(zpx.RBV - TARGET_ZPX) > 50 or abs(zpy.RBV - TARGET_ZPY) > 50:
    print("\nRequested move exceeds 50 µm.  Run lock_hybrid() first, "
          "then re-execute this script.")
    raise SystemExit

print("\n--- Current beam position ---")
print(f"zpx: {zpx.RBV:.2f} µm")
print(f"zpy: {zpy.RBV:.2f} µm")

# Execute the move using the approved macro (includes logging, interlocks)
mov(zpx, TARGET_ZPX)
mov(zpy, TARGET_ZPY)

# Allow piezos a short time to settle
time.sleep(1)

print("\n--- New beam position ---")
print(f"zpx: {zpx.RBV:.2f} µm")
print(f"zpy: {zpy.RBV:.2f} µm")
print("\nBeam should now be centred on the particle.")