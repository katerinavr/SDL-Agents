import loca
import pandas as pd
import robotics as ro
from robotics import procedure as proc
import rack_status
import random

# Initialize hardware modules
c9 = ro.system.init('controller')
t8 = ro.system.init('temperature')
coater = ro.system.init('coater')

# Set processing parameters
temperature = random.randint(80, 120)  # Random temperature between 80-120°C
coating_speed = random.uniform(5, 20)  # Random coating speed between 5-20 mm/s

# Step 1: Prepare the substrate
c9.tool = 'substrate_tool'  # Pick up the Bernoulli substrate gripper tool
c9.position = loca.substrate_rack_seq[0, 0]  # Move to the first substrate in the rack
c9.set_output('substrate_tool', True)  # Activate vacuum to pick up the substrate
c9.move_axis('z', 0)  # Move the arm up
c9.position = loca.s_coater  # Move the substrate to the coating station
c9.set_output('coater_stage_vacuum', True)  # Activate vacuum on the coater stage
c9.set_output('substrate_tool', False)  # Release the substrate
c9.tool = None  # Drop off the substrate tool

# Step 2: Prepare the PEDOT:PSS solution (polymer A)
c9.tool = None  # Ensure no tool is attached
c9.position = loca.vial_rack[1, 2]  # Move to polymer A (PEDOT:PSS) in the vial rack
c9.set_output('gripper', True)  # Close the gripper to pick up the vial
c9.move_axis('z', 0)  # Move the arm up
c9.position = loca.clamp  # Move the vial to the clamp
c9.set_output('clamp', True)  # Close the clamp
c9.set_output('gripper', False)  # Open the gripper

# Step 3: Uncap the vial and aspirate the solution
uncap_position = c9.uncap(pitch=1.75, revs=3.0, vel=5000, accel=5000)
c9.aspirate_ml(0, 0.5)  # Aspirate 0.5 mL of PEDOT:PSS solution

# Step 4: Set up the coating process
t8.set_temp(1, temperature)  # Set the coating temperature
coater.position = 45  # Move coater blade to the starting position
coater.velocity = coating_speed  # Set the coating velocity

# Step 5: Dispense and coat
c9.position = loca.p_coater  # Move to the coating station
c9.dispense_ml(0, 0.2)  # Dispense 0.2 mL of PEDOT:PSS solution
coater.position = 75  # Move blade to coat the film

# Step 6: Clean up
c9.position = loca.clamp  # Move back to the clamp
c9.dispense_ml(0, 0.3)  # Dispense remaining solution back into the vial
c9.position = uncap_position  # Move to recap the vial
c9.cap(pitch=1.75, revs=3.0, torque_thresh=1000, vel=5000, accel=5000)
c9.set_output('clamp', False)  # Open the clamp
c9.set_output('gripper', True)  # Close the gripper to pick up the vial
c9.position = loca.vial_rack[1, 2]  # Move the vial back to its original position
c9.set_output('gripper', False)  # Release the vial

# Step 7: Remove the coated substrate
c9.tool = 'substrate_tool'  # Pick up the substrate tool
c9.position = loca.s_coater  # Move to the coating station
c9.set_output('coater_stage_vacuum', False)  # Deactivate vacuum on the coater stage
c9.set_output('substrate_tool', True)  # Activate vacuum to pick up the substrate
c9.move_axis('z', 0)  # Move the arm up
c9.position = loca.substrate_rack_seq[0, 1]  # Move the substrate to a new position in the rack
c9.set_output('substrate_tool', False)  # Release the substrate
c9.tool = None  # Drop off the substrate tool

print(f"PEDOT:PSS film created with the following parameters:")
print(f"Temperature: {temperature}°C")
print(f"Coating speed: {coating_speed:.2f} mm/s")
