# filename: create_polymer_film.py
import loca
import robotics as ro
from robotics import procedure as proc

# Initialize the robot controller
c9 = ro.system.init('controller')

# Step 1: Move the substrate to the coating station
# Set the tool to the Bernoulli substrate gripper
c9.tool = 'substrate_tool'  # Ensure the correct tool is set

# Move to the position of the substrate (top-left position of the substrate rack)
c9.position = loca.substrate_rack_seq[0, 0]

# Activate the vacuum to pick up the substrate
c9.set_output('substrate_tool', True)

# Move to the coating station position
c9.position = loca.p_coater

# Activate the vacuum on the coating station to hold the substrate
c9.set_output('coater_stage_vacuum', True)

# Deactivate the vacuum of the Bernoulli tool to release the substrate at the coating station
c9.set_output('substrate_tool', False)

# Return the Bernoulli tool back to its initial location
c9.tool = None  # Drop off the Bernoulli tool

# Step 2: Move the vial with PEDOT:PSS to the clamp holder
# Define the polymer label
polymer_label = 'polymer_A'  # This corresponds to PEDOT:PSS

# Find the index of the vial containing the polymer
vial_index = proc.find_rack_index('vial', polymer_label)

# Move to the vial position
c9.position = loca.vial_rack[vial_index]

# Close the gripper to pick up the vial
c9.set_output('gripper', True)

# Move to the clamp holder position
c9.position = loca.clamp


# Step 3: Uncap the vial
c9.uncap(pitch=1.75, revs=3.0, vel=5000, accel=5000)  # Uncap the vial

# Step 4: Aspirate the polymer
proc.new_pipette(c9)  # Get a new pipette
c9.aspirate_ml(0, 0.5)  # Aspirate 0.5 mL of PEDOT:PSS

# Step 5: Move to the coating station to dropcast the polymer
c9.position = loca.p_coater  # Move to the coating station position
c9.dispense_ml(0, 0.5)  # Dispense the aspirated polymer

# Step 6: Remove the pipette
proc.remove_pipette(c9)  # Remove the pipette
