# filename: move_polymerA_to_clamp.py
import robotics as ro
from robotics import procedure as proc

# -------------------------------------------------
# 1.  Initialise the controller channel (approved call)
# -------------------------------------------------
c9 = ro.get_channel('c9')          # grab the N9 controller handle

# -------------------------------------------------
# 2.  Verify that the vial is present
# -------------------------------------------------
vial_df = ro.runtime['rack_status']['vial']      # DataFrame of vial contents
if not ((vial_df == 'polymer_A').any().any()):   # fast, DataFrame-safe search
    print("Experiment cannot be initiated.")
    ro.abort()                                   # tidy shutdown
    raise SystemExit

# -------------------------------------------------
# 3.  Locate the vial in the rack
# -------------------------------------------------
vial_idx = proc.find_rack_index('vial', 'polymer_A')   # returns (row, col)

# -------------------------------------------------
# 4.  Move the vial to the clamp
#     – Use the highest-level helper available; fall back if it is absent.
# -------------------------------------------------
if hasattr(proc, 'transfer_vial_to_clamp'):
    # One-liner convenience function (if provided in your API)
    proc.transfer_vial_to_clamp(
        controller=c9,
        rack_name='vial',
        rack_index=vial_idx,
        close_clamp=True
    )
else:
    # Standard two-step sequence with approved primitives
    proc.pick_vial(
        controller=c9,
        rack_name='vial',
        rack_index=vial_idx
    )
    proc.place_in_clamp(
        controller=c9,
        close_clamp=True
    )

# -------------------------------------------------
# 5.  Finished
# -------------------------------------------------
print("polymer_A vial successfully moved to clamp holder.")