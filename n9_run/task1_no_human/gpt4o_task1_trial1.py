# filename: move_vial_to_clamp.py

# Import necessary modules
import loca  # Ensure this module is defined and available
import robotics as ro
from robotics import procedure as proc

# Initialize the robot controller
try:
    c9 = ro.system.init('controller')
except Exception as e:
    print(f"Error initializing robot controller: {e}")
    exit(1)

# Identify the location of polymer A in the vial rack
try:
    vial_index = proc.find_rack_index('vial', 'polymer_A')
except Exception as e:
    print(f"Error finding vial index: {e}")
    exit(1)

# Move the robot arm to the location of polymer A
try:
    c9.position = loca.vial_rack[vial_index]
except Exception as e:
    print(f"Error moving to vial location: {e}")
    exit(1)

# Use the gripper to pick up the vial
try:
    c9.set_output('gripper', True)  # Close the gripper to pick up the vial
except Exception as e:
    print(f"Error operating gripper: {e}")
    exit(1)

# Move the robot arm to the clamp holder
try:
    c9.position = loca.clamp
except Exception as e:
    print(f"Error moving to clamp location: {e}")
    exit(1)

# Place the vial in the clamp holder
try:
    c9.set_output('clamp', False)  # Open the clamp to let the vial get in
    c9.set_output('clamp', True)   # Close the clamp to hold the vial
    c9.set_output('gripper', False)  # Open the gripper to release the vial
except Exception as e:
    print(f"Error operating clamp or gripper: {e}")
    exit(1)
