# Analysis

# 1. Nano-diffraction image
#    • The brightest diffraction signal is the small ~2 × 2 µm spot in the upper-left quadrant, centred at roughly (zpx, zpy) ≈ (-41 µm, +46 µm).
#    • Other spots (≈ 25, 18 µm and ≈ 5, -18 µm) are weaker.

# 2. Nano-fluorescence image

# 2. Nano-fluorescence image
# 2. Nano-fluorescence image
#    • The upper-left corner around (-41, +46) µm is relatively dark, i.e. few particles → no large (>10 µm) cluster.
#    • The regions near (25, 18) µm and (0, -20) µm sit inside bright, extended fluorescence clusters – they should be avoided.

# Conclusion
# The particle at (-41 µm, +46 µm) diffracts strongest and lies in an isolated, low-fluorescence area.
# Move the X-ray beam to:

#     zpx = –41 µm
#     zpy = +46 µm

# (±1 µm precision is sufficient.)

"""
Move the hybrid piezo stack so the micro-beam is centred on the
strongest, isolated nano-diffraction particle found at:

    zpx = –41 µm
    zpy = +46 µm
"""

import time
import epics
from epics import Device, Motor

# ------------------------------------------------------------------
# (1) Ensure the standard Device / Motor handles are present
# ------------------------------------------------------------------
if 'zpx' not in globals():
    zpx = Device('26idcnpi:X_HYBRID_SP.', attrs=('VAL', 'DESC'))
    zpx.add_pv('26idcnpi:m34.RBV', attr='RBV')

if 'zpy' not in globals():
    zpy = Device('26idcnpi:Y_HYBRID_SP.', attrs=('VAL', 'DESC'))
    zpy.add_pv('26idcnpi:m35.RBV', attr='RBV')

# large-travel optics / sample motors (only imported if missing)
if 'fomx' not in globals():
    fomx = Motor('26idcnpi:m10.')
if 'fomy' not in globals():
    fomy = Motor('26idcnpi:m11.')
if 'samy' not in globals():
    samy = Motor('26idcnpi:m17.')

if 'twotheta' not in globals():
    twotheta = Motor('26idcSOFT:sm3.')

# ------------------------------------------------------------------
# (2) Ensure not_epics_motors list exists (future-proof)
# ------------------------------------------------------------------
if 'not_epics_motors' not in globals():
    not_epics_motors = [zpx.NAME, zpy.NAME, twotheta.NAME]

# ------------------------------------------------------------------
# (3) Provide the standard “mov” helper if it is missing
# ------------------------------------------------------------------
if 'mov' not in globals():
    def mov(motor, position):
        """
        Beamline-compliant absolute move with all safety interlocks.
        Copied (and slightly generalised) from S26_commandline.py
        """
        # ------------------------------------------------------------------
        # 3a. Stop hybrid piezos when large stages are about to move
        # ------------------------------------------------------------------
        if motor.NAME in [fomx.NAME, fomy.NAME, samy.NAME]:
            epics.caput('26idcnpi:m34.STOP', 1)
            epics.caput('26idcnpi:m35.STOP', 1)
            epics.caput('26idcSOFT:userCalc1.SCAN', 0)
            epics.caput('26idcSOFT:userCalc3.SCAN', 0)

        # ------------------------------------------------------------------
        # 3b. Protect against unlocked hybrid piezos (>100 µm offset)
        # ------------------------------------------------------------------
        if motor.NAME in [zpx.NAME, zpy.NAME]:
            if abs(zpx.RBV - zpx.VAL) > 100 or abs(zpy.RBV - zpy.VAL) > 100:
                print("Please run lock_hybrid() before moving the piezos!")
                return

        # ------------------------------------------------------------------
        # 3c. Perform the motion (hybrid piezos vs. real motors)
        # ------------------------------------------------------------------
        desc = motor.DESC or motor.NAME   # DESC may be None if not connected
        if motor.NAME in not_epics_motors:
            motor.VAL = position
            time.sleep(1.0)
            print(f"{desc} ---> {motor.RBV:.2f} µm")
        else:
            result = motor.move(position, wait=True)
            if result == 0:
                time.sleep(0.5)
                print(f"{desc} ---> {motor.RBV:.3f}")
                # Write to logbook if the session defined it
                if 'logbook' in globals():
                    with open(logbook, "a") as fp:
                        fp.write(f"{desc} ---> {motor.RBV:.3f}\n")
                epics.caput('26idcSOFT:userCalc1.SCAN', 6)
                epics.caput('26idcSOFT:userCalc3.SCAN', 6)
            else:
                raise RuntimeError("Motion failed")

# ------------------------------------------------------------------
# (4) Extra one-shot hybrid-lock check before we start
# ------------------------------------------------------------------
if abs(zpx.RBV - zpx.VAL) > 100 or abs(zpy.RBV - zpy.VAL) > 100:
    raise RuntimeError(
        "Hybrid piezos are >100 µm from their actuators. "
        "Please lock_hybrid() before running this script."
    )

# ------------------------------------------------------------------
# (5) Move to the desired coordinates
# ------------------------------------------------------------------
TARGET_X = -41.0    # µm (negative = inboard)
TARGET_Y =  46.0    # µm (positive = up)

print(f"Moving beam to the best-diffracting particle "
      f"at ({TARGET_X:+.1f} µm, {TARGET_Y:+.1f} µm) …")
mov(zpx, TARGET_X)
mov(zpy, TARGET_Y)
print("Done – beam is now centred on the selected particle.")