# filename: create_pedot_pss_film.py

import loca  # location information
import pandas as pd
import robotics as ro
from robotics import procedure as proc
import rack_status

# Initialize hardware modules
c9 = ro.system.init('controller')  # N9 robot controller
t8 = ro.system.init('temperature')  # temperature controller
coater = ro.system.init('coater')  # coating station

# Set the coating temperature
T = 90  # Coating temperature in Celsius
t8.set_temp(1, T)

# Move solution from the vial rack to the clamp
sol_label = 'polymer_A'  # PEDOT:PSS is defined as polymer A
vial_index = proc.find_rack_index('vial', sol_label)
c9.position = loca.vial_rack[vial_index]  # Move robot arm to the solution

# Pick up the vial
c9.set_output('gripper', True)  # Close the gripper to pick up the vial
c9.position = loca.clamp  # Move robot arm to the clamp
c9.set_output('clamp', True)  # Close the clamp to hold the vial
c9.set_output('gripper', False)  # Open the gripper to release the vial

# Uncap the vial
uncap_position = c9.uncap(pitch=1.75, revs=3.0, vel=5000, accel=5000)  # Uncap the vial and record the position
c9.position = uncap_position  # Move gripper back to the recorded position

# Aspirate the solution in the clamp
c9.aspirate_ml(0, 0.5)  # Aspirate 0.5mL
c9.dispense_ml(0, 0.2)  # Dispense 0.2mL

# Move to the coater
c9.position = loca.p_coater  # Move pipette to the coating station

# Set coater parameters
coater.position = 45  # Move coater blade to the starting position
coater.velocity = 1  # Set the coating velocity to 1 mm/s

# Perform the coating
coater.position = 75  # Move blade all the way to the right

# Post-processing
# Set post-processing temperature and speed
post_temp = 60  # Post-processing temperature in Celsius
post_speed = 1  # Post-processing speed in mm/s
t8.set_temp(1, post_temp)

# Return solution in clamp back to the vial rack
c9.position = loca.clamp  # Move robot arm to the clamp
c9.position = loca.vial_rack[vial_index]  # Move robot arm to the solution

# Return sample to rack, end of experiment
c9.position = loca.s_coater
c9.position = loca.substrate_rack_seq[0, 0]  # Move substrate to the substrate rack (top-left position)

# Deactivate vacuum and gripper
c9.set_output('substrate_tool', False)  # Deactivate the vacuum on the Bernoulli gripper
c9.set_output('gripper', False)  # Open the gripper to release the vial

print("Polymer film creation with PEDOT:PSS completed.")
