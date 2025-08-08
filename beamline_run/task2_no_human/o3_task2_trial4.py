# The single, bright diffraction spot is located very close to the co-ordinates

# • zpx ≈ 0 µm (±1 µm)
# • zpy ≈ –39 µm (±1 µm)

# Please move the X-ray beam to (zpx = 0 µm, zpy = –39 µm). Centering the beam there should place it directly on the isolated particle that is diffracting most strongly in this scan.


# filename: center_beam_to_particle.py
# Move the X-ray beam to the isolated particle at zpx = 0 µm, zpy = –39 µm

import time
import math   # only for isinstance check in fmt()

target_x = 0.0      # µm
target_y = -39.0    # µm

def fmt(val):
    """Return a value nicely formatted to two decimals, falling back to str() if not a number."""
    try:
        return f"{float(val):.2f}"
    except (TypeError, ValueError):
        return str(val)

# ------------------------------------------------------------------
# 1) Make sure the piezo hybrid stage is still “locked” as per beam-line rule
if (abs(zpx.RBV - zpx.VAL) > 100) or (abs(zpy.RBV - zpy.VAL) > 100):
    print("Please use lock_hybrid() to lock piezos at current position first … Aborting move.")
else:
    # ------------------------------------------------------------------
    # 2) Report current position
    print(f"Current hybrid stage position :  zpx = {fmt(zpx.RBV)} µm ,  zpy = {fmt(zpy.RBV)} µm")
    print(f"Moving beam to                :  zpx = {target_x:.2f} µm ,  zpy = {target_y:.2f} µm")

    # 3) Perform absolute moves via the standard mov() helper
    mov(zpx, target_x)
    mov(zpy, target_y)

    # 4) Final read-back / confirmation
    time.sleep(0.5)   # allow PVs to settle
    print(f"New hybrid stage position     :  zpx = {fmt(zpx.RBV)} µm ,  zpy = {fmt(zpy.RBV)} µm")
    print("Beam centred on the isolated diffracting particle.")