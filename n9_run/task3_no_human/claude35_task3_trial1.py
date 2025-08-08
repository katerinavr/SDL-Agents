import random
import logging
import loca
import robotics as ro
from robotics import procedure as proc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PolymerFilm:
    def __init__(self, polymer_name, temperature, coating_speed):
        self.polymer_name = polymer_name
        self.temperature = temperature
        self.coating_speed = coating_speed

    def create_film(self, c9, t8, coater):
        logger.info(f"Creating {self.polymer_name} film:")

        # Set temperature
        logger.info(f"Setting temperature to {self.temperature:.2f}°C")
        t8.set_temp(1, self.temperature)

        # Set coating speed
        logger.info(f"Setting coating speed to {self.coating_speed:.2f} mm/s")
        coater.velocity = self.coating_speed

        # Get polymer solution
        logger.info("Getting polymer solution")
        vial_index = proc.find_rack_index('vial', 'polymer_A')
        c9.position = loca.vial_rack[vial_index]
        c9.set_output('gripper', True)
        c9.move_axis('z', 0)
        c9.position = loca.clamp
        c9.set_output('clamp', True)
        c9.set_output('gripper', False)

        # Uncap vial
        logger.info("Uncapping vial")
        uncap_position = c9.uncap(pitch=1.75, revs=3.0, vel=5000, accel=5000)

        # Aspirate solution
        logger.info("Aspirating polymer solution")
        c9.aspirate_ml(0, 0.5)

        # Get substrate
        logger.info("Getting substrate")
        c9.tool = 'substrate_tool'
        c9.position = loca.substrate_rack_seq[0, 0]
        c9.set_output('substrate_tool', True)
        c9.move_axis('z', 0)

        # Place substrate on coater
        logger.info("Placing substrate on coater")
        c9.position = loca.s_coater
        c9.set_output('coater_stage_vacuum', True)
        c9.set_output('substrate_tool', False)
        c9.tool = None

        # Dispense solution
        logger.info("Dispensing polymer solution")
        c9.position = loca.p_coater
        c9.dispense_ml(0, 0.2)

        # Coat film
        logger.info("Coating process started")
        coater.position = 45
        coater.position = 75

        logger.info("Waiting for the film to dry")
        # In a real scenario, we would wait for the appropriate drying time here

        logger.info("Film creation completed")

        # Clean up
        c9.position = loca.clamp
        c9.position = loca.vial_rack[vial_index]
        c9.cap(pitch=1.75, revs=3.0, torque_thresh=1000, vel=5000, accel=5000)
        c9.set_output('gripper', False)
        c9.move_axis('z', 0)

def create_pedot_pss_film(temp_range, speed_range, c9, t8, coater):
    if temp_range[0] >= temp_range[1] or speed_range[0] >= speed_range[1]:
        raise ValueError("Invalid range: min value must be less than max value")

    polymer_a = "PEDOT:PSS"
    temperature = round(random.uniform(temp_range[0], temp_range[1]), 2)
    coating_speed = round(random.uniform(speed_range[0], speed_range[1]), 2)

    film = PolymerFilm(polymer_a, temperature, coating_speed)
    film.create_film(c9, t8, coater)

    return film

# Initialize robot components
c9 = ro.system.init('controller')
t8 = ro.system.init('temperature')
coater = ro.system.init('coater')

# Example usage (replace with actual values from the paper)
temp_range = (60, 120)  # Replace with actual range from the paper
speed_range = (5, 20)   # Replace with actual range from the paper

try:
    created_film = create_pedot_pss_film(temp_range, speed_range, c9, t8, coater)

    logger.info(f"\nFilm created with the following parameters:")
    logger.info(f"Polymer: {created_film.polymer_name}")
    logger.info(f"Temperature: {created_film.temperature:.2f}°C")
    logger.info(f"Coating speed: {created_film.coating_speed:.2f} mm/s")
except ValueError as e:
    logger.error(f"Error creating film: {e}")

logger.info("Experiment completed.")
