# filename: combined_script.py
import pandas as pd
import loca
import robotics as ro
from robotics import procedure as proc

# Initialize rack_status in the runtime
ro.runtime['rack_status'] = {
    'vial': pd.DataFrame(
        [
            ['water_gap', 'NaCl', None, None, None, None, None, None],
            [False, None, 'polymer_A', None, None, None, None, None],
            [False, None, None, 'carbon_black', None, None, None, None],
            [None, None, False, None, None, None, None, None],
            [None, None, False, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ]
    ),
    'substrate': pd.DataFrame(
        [
            ['new', 'new', 'new', 'new', 'new', 'new'],
            ['new', 'new', 'new', 'new', 'new', 'new'],
            ['new', 'new', 'new', 'new', 'new', 'new'],
            ['new', 'new', 'new', 'new', 'new', 'new'],
            ['new', 'new', 'new', 'new', 'new', 'new'],
            ['new', 'new', 'new', 'new', 'new', 'new'],
            ['new', 'new', 'new', 'new', 'new', 'new'],
            ['new', 'new', 'new', 'new', 'new', 'new'],
            ['new', 'new', 'new', 'new', 'new', 'new'],
            ['new', 'new', 'new', 'new', 'new', 'new'],
            ['new', 'new', 'new', 'new', 'new', 'new'],
            ['new', 'new', 'new', 'new', 'new', 'new'],
        ]
    ),
}

print("rack_status initialized successfully.")

# Initialize the robot controller
c9 = ro.system.init('controller')

# Access the rack status to find the location of polymer A
rack_status = ro.runtime['rack_status']
vial_rack = rack_status['vial']

# Identify the location of polymer A in the vial rack
vial_index = proc.find_rack_index('vial', 'polymer_A')

# Move the robot arm to the location of polymer A
c9.position = vial_rack.iloc[vial_index]

# Pick up the vial using the gripper
c9.set_output('gripper', True)  # Close the gripper to pick up the vial

# Move the robot arm to the clamp holder
c9.position = loca.clamp

# Place the vial in the clamp holder
c9.set_output('clamp', True)  # Close the clamp to hold the vial
c9.set_output('gripper', False)  # Open the gripper to release the vial

# Return the gripper to the starting position
c9.position = [0, 0, 0, 0]  # Move robot arm to the initial location