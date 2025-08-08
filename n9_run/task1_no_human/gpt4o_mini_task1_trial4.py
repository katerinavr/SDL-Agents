# filename: move_vial_to_clamp.py
import loca
import robotics as ro
from robotics import procedure as proc

# Initialize the robot controller
c9 = ro.system.init('controller')

# Define the polymer label for PEDOT:PSS
polymer_label = 'polymer_A'  # Ensure this matches the expected label in the system

# Step 1: Find the index of the vial containing polymer A
vial_index = proc.find_rack_index('vial', polymer_label)

# Step 2: Move to the vial position
c9.position = loca.vial_rack[vial_index]

# Step 3: Pick up the vial
c9.set_output('gripper', True)  # Close the gripper to pick up the vial

# Step 4: Move to the clamp holder position
c9.position = loca.clamp

# Step 5: Release the vial into the clamp holder
c9.set_output('gripper', False)  # Open the gripper to release the vial