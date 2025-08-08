# filename: move_polymer_A_to_clamp.py
# --------------------------------------------------------------
# Collision-safe transfer of the vial labelled polymer_A
# (PEDOT:PSS) from the vial rack to the clamp holder.
# Uses ONLY the objects / motion primitives exposed by the
# PolyBot bundle that is pre-loaded in the runtime.
# --------------------------------------------------------------

from polybot import ro, loca, proc, c9       # <- single sanctioned import

def move_polymer_A_to_clamp():
    label = "polymer_A"                      # PEDOT:PSS vial label

    # ── 1  Availability check ────────────────────────────────────────────
    if label not in ro.runtime["rack_status"]["vial"].values:
        print("Experiment cannot be initiated.")       # mandatory wording
        return

    # ── 2  Rack indices & predefined safe poses ──────────────────────────
    row, col = proc.find_rack_index("vial", label)     # (row, col)

    # These pose maps are defined in the starter PolyBot file
    above_vial   = loca.vial_rack_approach[row][col]   # safe overhead point
    pick_vial    = loca.vial_rack_pick[row][col]       # pick height
    above_clamp  = loca.clamp_approach                 # safe overhead point
    insert_clamp = loca.clamp_insert                   # insert height

    # ── 3  Motion parameters (units = mm s⁻¹) ────────────────────────────
    vel_xy = 150        # horizontal moves
    vel_z  = 150        # vertical moves

    # ── 4  Pick the vial ─────────────────────────────────────────────────
    c9.set_output("gripper", False)                    # open gripper
    c9.move_linear(above_vial,   vel=vel_xy)           # approach rack well
    c9.move_linear(pick_vial,    vel=vel_xy)           # descend to pick height
    c9.set_output("gripper", True)                     # grip vial
    c9.move_linear(above_vial,   vel=vel_z)            # lift back to overhead

    # ── 5  Place the vial into the clamp ─────────────────────────────────
    c9.move_linear(above_clamp,  vel=vel_xy)           # approach clamp
    c9.set_output("clamp", False)                      # open clamp
    c9.move_linear(insert_clamp, vel=vel_xy)           # descend to insert height
    c9.set_output("clamp", True)                       # secure vial
    c9.set_output("gripper", False)                    # release gripper
    c9.move_linear(above_clamp,  vel=vel_z)            # retract to overhead

    # ── 6  Completion message ────────────────────────────────────────────
    print("polymer_A vial successfully transferred to the clamp holder.")

# ------------------------------------------------------------------------
# Execute once
# ------------------------------------------------------------------------
move_polymer_A_to_clamp()