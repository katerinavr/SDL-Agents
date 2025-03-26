# filename: move_substrate_to_coating_station.py
import loca
import robotics as ro

try:
    # Initialize the robot controller
    c9 = ro.system.init('controller')

    # Pick up the substrate using the Bernoulli substrate gripper tool
    c9.tool = 'substrate_tool'  # Pick up the Bernoulli substrate gripper tool
    c9.set_output('substrate_tool', True)  # Activate the vacuum to pick up the substrate

    # Move the robot arm to the substrate rack and pick up a substrate
    c9.position = loca.substrate_rack_seq[0, 0]  # Move to the top-left position of the substrate rack

    # Move the substrate to the coating station
    c9.position = loca.s_coater  # Move to the coating station

    # Place the substrate on the coater stage and activate the vacuum to hold it in place
    c9.set_output('coater_stage_vacuum', True)  # Activate the vacuum on the coater stage
    c9.set_output('substrate_tool', False)  # Deactivate the vacuum to release the substrate

    # Drop off the Bernoulli substrate gripper tool
    c9.tool = None  # Drop off the tool in the gripper

except Exception as e:
    print(f"An error occurred: {e}")