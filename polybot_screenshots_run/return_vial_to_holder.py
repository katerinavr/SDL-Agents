# filename: return_vial_to_holder.py
import loca
import robotics as ro
from robotics import procedure as proc
import rack_status  # Ensure rack_status is imported

# Initialize the robot controller
c9 = ro.system.init('controller')

# Access the rack status to find the location of polymer A
rack_status = ro.runtime['rack_status']
vial_rack = rack_status['vial']

# Identify the location of polymer A in the vial rack
vial_index = proc.find_rack_index('vial', 'polymer_A')

# Move the robot arm to the clamp holder
c9.position = loca.clamp

# Pick up the vial using the gripper
c9.set_output('clamp', False)  # Open the clamp to release the vial
c9.set_output('gripper', True)  # Close the gripper to pick up the vial

# Move the robot arm to the original location of polymer A in the vial rack
c9.position = loca.vial_rack[vial_index]

# Place the vial back in the vial rack
c9.set_output('gripper', False)  # Open the gripper to release the vial