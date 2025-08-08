# filename: scan_100um.py
#
# 100 µm × 100 µm fly-scan   –   1 µm steps, 0.01 s dwell
# -----------------------------------------------------------------
# USAGE
#   /APSshare/anaconda/x86_64/bin/ipython -i scan_100um.py
#      (works whether or not you previously loaded S26_commandline.py)
# -----------------------------------------------------------------

# Pull in all approved utilities and motor definitions
from S26_commandline import *          # detectors(), fly2d(), lock_hybrid(), …

# 1) Select the detectors that should be triggered at every point
detectors(['scaler', 'xrf'])           # add/remove detectors as required

# 2) Make sure the hybrid piezos are “locked” so they do not jump
lock_hybrid()

# 3) Launch the 2-D fly-scan
#    • Outer loop (step mode, Y axis = zpy) : 101 pts  → 1 µm pitch
#    • Inner loop (fly  mode, X axis = zpx) : 100 pts  → 1 µm pitch
#      (For the fly axis step size = (end – start) / NPTS)
#    • Exposure time                        : 0.01 s
fly2d(
    zpy,  -50,  +50,  101,          # Y-axis : ±50 µm, 1 µm steps
    zpx,  -50,  +50,  100,          # X-axis : ±50 µm, 1 µm steps
    0.01,                            # dwell time per point [s]
    absolute=False                   # positions are relative to current coords
)