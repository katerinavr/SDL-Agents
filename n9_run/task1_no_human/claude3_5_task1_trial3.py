# filename: move_polymer_A_to_clamp.py

import loca
import robotics as ro
from robotics import procedure as proc
import time

# Initialize the robot controller
c9 = ro.system.init('controller')

# Step 1: Find the rack index for polymer_A
vial_index = proc.find_rack_index('vial', 'polymer_A')
print(f"Vial index for polymer_A: {vial_index}")

# Step 2: Move the robot arm to the vial position
c9.position = loca.vial_rack[vial_index]
print("Moved to vial position")

# Step 3: Pick up the vial using the gripper
c9.set_output('gripper', True)
time.sleep(0.5)  # Wait for gripper to close
print("Gripper closed")

# Check if vial is gripped successfully
if not c9.get_input('gripper_sensor'):
    raise Exception("Failed to grip the vial. Please check and try again.")

# Step 4: Move the vial to the clamp position
c9.move_axis('z', 0)  # Move up to avoid collisions (0 is assumed to be the highest safe position)
print("Moved up")
c9.position = loca.clamp
print("Moved to clamp position")

# Step 5: Place the vial in the clamp and secure it
c9.set_output('clamp', False)  # Open the clamp
time.sleep(0.5)  # Wait for clamp to open
print("Clamp opened")

# Move down by 5 cm (50,000 micrometers)
c9.move_axis('z', c9.position[3] - 50000, vel=15000)  # Units are in micrometers
print("Moved down")

c9.set_output('gripper', False)  # Release the vial
time.sleep(0.5)  # Wait for gripper to open
print("Gripper opened")

c9.move_axis('z', c9.position[3] - 5000)  # Move up slightly (5,000 micrometers)
print("Moved up slightly")

c9.set_output('clamp', True)  # Close the clamp
time.sleep(0.5)  # Wait for clamp to close
print("Clamp closed")

# Final position check
if not c9.get_input('clamp_sensor'):
    raise Exception("Vial may not be properly secured in the clamp. Please check and try again.")

print("PEDOT:PSS (polymer_A) vial has been successfully moved to the clamp holder.")
