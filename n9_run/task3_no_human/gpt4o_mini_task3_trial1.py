# filename: create_polymer_film.py

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
sol_label = 'polymer_A'
vial_index = proc.find_rack_index('vial', sol_label)
c9.position = loca.vial_rack[vial_index]  # move robot arm to the solution

# Pick up the vial
c9.set_output('gripper', True)  # close the gripper to pick up the vial
c9.position = loca.clamp  # move robot arm to the clamp
c9.set_output('clamp', True)  # close the clamp to hold the vial
c9.set_output('gripper', False)  # open the gripper to release the vial

# Uncap the vial
uncap_position = c9.uncap(pitch=1.75, revs=3.0, vel=5000, accel=5000)  # uncap the vial and record the position
c9.position = uncap_position  # move gripper back to the recorded position

# Aspirate the solution in the clamp
c9.aspirate_ml(0, 0.5)  # aspirate 0.5mL

# Move to the coater and dispense the solution
c9.position = loca.p_coater  # move pipette to the coating station
c9.dispense_ml(0, 0.5)  # dispense 0.5mL

# Set coater parameters and start coating
coater.position = 45  # move coater blade to the starting position
coater.velocity = 1  # set the coating velocity to 1 mm/s
coater.position = 75  # move blade all the way to the right

# Post-processing: solvent rinsing
# Assuming the solvent is already prepared and in the system
c9.position = loca.p_coater  # move pipette to the coating station
c9.aspirate_ml(0, 0.5)  # aspirate 0.5mL of solvent
c9.dispense_ml(0, 0.5)  # dispense 0.5mL over the film
# Repeat rinsing if necessary

# Return solution in clamp back to the vial rack
c9.position = loca.clamp  # move robot arm to the clamp
c9.position = loca.vial_rack[vial_index]  # move robot arm to the solution

# End of experiment
c9.position = loca.s_coater
c9.position = loca.substrate_rack_seq[0, 0]  # move substrate to the substrate rack (top-left position)
