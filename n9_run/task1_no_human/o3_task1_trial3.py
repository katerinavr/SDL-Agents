import loca
import robotics as ro
from robotics import procedure as proc

def _find_polymer_index() -> int | None:
    """
    Return the flat rack index of the PEDOT:PSS vial, or None if not present.
    """
    idx = proc.find_rack_index('vial', 'PEDOT:PSS')
    if idx is None:                        # optional fallback
        idx = proc.find_rack_index('vial', 'polymer_A')
    return idx

def main() -> None:
    # ------------------------------------------------------------------
    # 1. Locate the vial
    vial_index = _find_polymer_index()
    if vial_index is None:
        print("Experiment cannot be initiated.")
        return
    print(f"PEDOT:PSS vial located at rack index {vial_index}")

    # ------------------------------------------------------------------
    # 2. Retrieve device handles
    c9     = ro.get_device('robot_arm')    # robot arm / gripper
    clamp  = ro.get_device('clamp')        # independent clamp device

    # ------------------------------------------------------------------
    # 3. Pick up the vial from the rack
    c9.gripper.open()
    c9.move_linear(loca.vial_rack[vial_index])     # approach vial
    c9.gripper.close()                             # grasp
    c9.move_axis_relative('z', +9000, vel=15000)   # lift 9 cm

    # ------------------------------------------------------------------
    # 4. Transfer to clamp holder
    clamp.open()                                   # ensure jaws open
    proc.assert_device_state('clamp', 'open')      # safety interlock

    c9.move_linear(loca.clamp)                     # move into clamp area
    clamp.close()                                  # secure vial
    c9.gripper.open()                              # release vial
    c9.move_axis_relative('z', +5000, vel=15000)   # retreat 5 cm

    print("Vial containing PEDOT:PSS successfully placed in the clamp holder.")

# Allow direct execution if not run via the dispatcher
if __name__ == "__main__":
    main()