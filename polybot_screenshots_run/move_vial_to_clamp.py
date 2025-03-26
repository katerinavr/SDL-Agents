# filename: move_vial_to_clamp.py
import loca
import robotics as ro
from robotics import procedure as proc
import rack_status  # Ensure rack_status is imported

# Initialize the robot controller
c9 = ro.system.init('controller')

# Ensure rack_status is correctly initialized in ro.runtime
if 'rack_status' not in ro.runtime:
    ro.runtime['rack_status'] = rack_status

# Access the rack status to find the location of polymer A
vial_rack = ro.runtime['rack_status']['vial']

# Identify the location of polymer A in the vial rack
vial_index = proc.find_rack_index('vial', 'polymer_A')

# Move the robot arm to the location of polymer A
c9.position = loca.vial_rack[vial_index]

# Pick up the vial using the gripper
c9.set_output('gripper', True)  # Close the gripper to pick up the vial

# Move the robot arm to the clamp holder
c9.position = loca.clamp

# Place the vial in the clamp holder
c9.set_output('clamp', True)  # Close the clamp to hold the vial
c9.set_output('gripper', False)  # Open the gripper to release the vial