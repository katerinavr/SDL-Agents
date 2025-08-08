# filename: move_vial_to_clamp.py
import loca
import robotics as ro
from robotics import procedure as proc

# Initialize the robot controller
try:
    c9 = ro.system.init('controller')
except Exception as e:
    print(f"Error initializing controller: {e}")
    exit(1)

# Define the polymer label
polymer_label = 'polymer_A'

# Find the index of the vial containing polymer A
vial_index = proc.find_rack_index('vial', polymer_label)
if vial_index is None:
    print(f"Vial with label {polymer_label} not found.")
    exit(1)

# Move robot arm to the vial position
try:
    c9.position = loca.vial_rack[vial_index]
except IndexError:
    print(f"Invalid vial index: {vial_index}. Check the vial rack.")
    exit(1)

# Close the gripper to pick up the vial
if not c9.set_output('gripper', True):
    print("Failed to close the gripper.")
    exit(1)

# Move robot arm to the clamp holder position
c9.position = loca.clamp

# Open the gripper to release the vial into the clamp holder
if not c9.set_output('gripper', False):
    print("Failed to open the gripper.")
    exit(1)

print("Vial with PEDOT:PSS has been successfully moved to the clamp holder.")
