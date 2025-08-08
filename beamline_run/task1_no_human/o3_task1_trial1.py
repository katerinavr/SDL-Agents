# filename: scan_100um_area.py
"""
100 µm × 100 µm raster, 1 µm resolution, 0.01 s exposure.

Outer loop (step):   zpy  → 101 points  (-50 … +50 µm, 1 µm steps)
Inner loop (fly):    zpx  → 100 points  (-50 … +50 µm, 1 µm steps)

The script is meant to be executed in an IPython session that has already run
S26_commandline.py, so all motors and helper functions are defined.
"""

fly2d(
    motor1    = zpy,     startpos1 = -50,  endpos1 =  50,  numpts1 = 101,   # outer loop (step)
    motor2    = zpx,     startpos2 = -50,  endpos2 =  50,  numpts2 = 100,   # inner loop (fly)
    dettime   = 0.01,                                                   # exposure per point (s)
    absolute  = False                                                   # offsets relative to current pos
)


# --------------------------------------------------------------------------
# (1) Ensure the helper functions and motors are available in this namespace
# --------------------------------------------------------------------------
try:
    detectors        # noqa: F401  (just probing for NameError)
except NameError:
    # We are probably being run with “ipython -i S26_commandline.py ...”
    # In that case the symbols live in __main__; import them explicitly.
    from __main__ import detectors, fly2d, zpx, zpy

# --------------------------------------------------------------------------
# (2) Select detectors and set exposure time
# --------------------------------------------------------------------------
detectors_to_use = ['scaler']       # add 'xrf', 'andor', 'pilatus', … if needed
detectors(detectors_to_use)

# --------------------------------------------------------------------------
# (3) Launch the 2-D fly scan
# --------------------------------------------------------------------------
fly2d(
    motor1    = zpy,     startpos1 = -50,  endpos1 =  50,  numpts1 = 101,   # outer loop (step)
    motor2    = zpx,     startpos2 = -50,  endpos2 =  50,  numpts2 = 100,   # inner loop (fly)
    dettime   = 0.01,                                                   # exposure per point (s)
    absolute  = False                                                   # offsets relative to current pos
)

print("\nScan command issued.  Monitor the console for progress …")