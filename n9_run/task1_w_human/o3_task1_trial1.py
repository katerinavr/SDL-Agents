import loca                           # location data (rack & clamp poses)
import robotics as ro                 # N9 robotics interface
from robotics import procedure as proc

# -----------------------------------------------------------
# 1. Initialise the robot controller
c9 = ro.system.init('controller')     # N9 arm controller object

# -----------------------------------------------------------
# 2. Locate the vial containing PEDOT:PSS
VIAL_LABEL = 'polymer_A'
vial_index = proc.find_rack_index('vial', VIAL_LABEL)

if vial_index is None:
    # Required vial not found – abort experiment
    raise RuntimeError("Experiment cannot be initiated.")

print(f"'{VIAL_LABEL}' located at rack position {vial_index}.")

# -----------------------------------------------------------
# 3. Pick up the vial from the rack
print("Picking up the vial …")
c9.set_output('gripper', False)                     # ensure gripper open
c9.position = loca.vial_rack[vial_index]            # move above vial
c9.move_axis('z', c9.position[3] - 9000, vel=15000) # descend ≈9 cm
c9.set_output('gripper', True)                      # close gripper to grasp vial
c9.move_axis('z', 0)                                # lift fully upward

# -----------------------------------------------------------
# 4. Transfer the vial to the clamp holder
print("Placing vial into clamp holder …")
c9.set_output('clamp', False)                       # open clamp
c9.position = loca.clamp                            # move to clamp pose
c9.set_output('clamp', True)                        # close clamp to secure vial
c9.set_output('gripper', False)                     # release vial
c9.move_axis('z', 0)                                # retract arm safely

print("Vial 'polymer_A' successfully moved to clamp holder.")