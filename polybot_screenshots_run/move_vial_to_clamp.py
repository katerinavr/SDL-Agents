# filename: move_vial_to_clamp.py
import loca
import pandas as pd
import robotics as ro
from robotics import procedure as proc
import rack_status  # Import the rack_status module

# Initialize the robot controller
c9 = ro.system.init('controller')

# Access the rack status to find the location of polymer A
rack_status = ro.runtime['rack_status']
vial_rack = rack_status['vial']

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