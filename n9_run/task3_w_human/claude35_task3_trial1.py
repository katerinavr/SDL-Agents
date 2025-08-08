import loca
import pandas as pd
import robotics as ro
from robotics import procedure as proc
import rack_status
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define constants
COATING_TEMPERATURE = 80  # Celsius
COATING_SPEED = 10  # mm/s
SOLUTION_VOLUME = 0.2  # mL
DRYING_TIME = 300  # seconds
MAX_SAFE_TEMPERATURE = 120  # Celsius

# Initialize hardware modules
c9 = ro.system.init('controller')
t8 = ro.system.init('temperature')
coater = ro.system.init('coater')

def setup_coating_temperature(temperature):
    """
    Set up the coating temperature and perform a safety check.

    Args:
        temperature (float): The desired coating temperature in Celsius.

    Raises:
        ValueError: If the temperature exceeds the safe limit.
        Exception: For any other errors during temperature setting.
    """
    try:
        if temperature > MAX_SAFE_TEMPERATURE:
            raise ValueError(f"Temperature {temperature}°C exceeds safe limit of {MAX_SAFE_TEMPERATURE}°C")
        t8.set_temp(1, temperature)
        actual_temp = t8.get_temp(1)
        if abs(actual_temp - temperature) > 2:
            raise ValueError(f"Failed to set temperature. Target: {temperature}°C, Actual: {actual_temp}°C")
        logging.info(f"Coating temperature set to {actual_temp}°C")
    except Exception as e:
        logging.error(f"Failed to set coating temperature: {e}")
        raise

def pick_up_substrate():
    """
    Pick up a substrate from the rack and place it on the coater stage.

    Raises:
        Exception: If any step in the substrate pickup process fails.
    """
    try:
        c9.tool = 'substrate_tool'
        c9.position = loca.substrate_rack_seq[0, 0]
        c9.set_output('substrate_tool', True)
        c9.move_axis('z', 0)
        c9.position = loca.s_coater
        c9.set_output('coater_stage_vacuum', True)
        c9.set_output('substrate_tool', False)
        c9.move_axis('z', 0)
        c9.tool = None
        if not c9.get_input('coater_stage_vacuum'):
            raise ValueError("Substrate not detected on coater stage")
        logging.info("Substrate picked up and placed on coater stage")
    except Exception as e:
        logging.error(f"Failed to pick up substrate: {e}")
        raise

def prepare_pedot_pss_solution():
    """
    Prepare the PEDOT:PSS solution for coating.

    Returns:
        tuple: The uncap position for later recapping.

    Raises:
        Exception: If any step in the solution preparation process fails.
    """
    try:
        c9.tool = None
        vial_index = proc.find_rack_index('vial', 'polymer_A')
        c9.position = loca.vial_rack[vial_index]
        c9.set_output('gripper', True)
        c9.move_axis('z', 0)
        c9.position = loca.clamp
        c9.set_output('clamp', False)
        c9.set_output('gripper', False)
        c9.set_output('clamp', True)
        uncap_position = c9.uncap(pitch=1.75, revs=3.0, vel=5000, accel=5000)
        logging.info("PEDOT:PSS solution prepared")
        return uncap_position
    except Exception as e:
        logging.error(f"Failed to prepare PEDOT:PSS solution: {e}")
        raise

def aspirate_and_dispense_solution():
    """
    Aspirate the PEDOT:PSS solution and dispense it onto the substrate.

    Raises:
        Exception: If aspiration or dispensing fails.
    """
    try:
        proc.new_pipette(c9)
        c9.position = loca.p_clamp
        c9.aspirate_ml(0, SOLUTION_VOLUME)
        c9.position = loca.p_coater
        c9.dispense_ml(0, SOLUTION_VOLUME)
        if abs(c9.get_syringe_volume(0) - 0) > 0.01:
            raise ValueError(f"Dispensing error. Residual volume: {c9.get_syringe_volume(0)} mL")
        logging.info(f"Aspirated and dispensed {SOLUTION_VOLUME} mL of PEDOT:PSS solution")
    except Exception as e:
        logging.error(f"Failed to aspirate and dispense solution: {e}")
        raise

def perform_blade_coating():
    """
    Perform the blade coating process.

    Raises:
        Exception: If the coating process fails or the coater doesn't reach the expected position.
    """
    try:
        coater.position = 45
        coater.velocity = COATING_SPEED
        coater.position = 75
        if abs(coater.position - 75) > 1:
            raise ValueError(f"Coater failed to reach final position. Current position: {coater.position}")
        logging.info(f"Blade coating performed at {COATING_SPEED} mm/s")
    except Exception as e:
        logging.error(f"Failed to perform blade coating: {e}")
        raise

def return_substrate_to_rack():
    """
    Return the coated substrate to the rack.

    Raises:
        Exception: If any step in returning the substrate fails.
    """
    try:
        c9.tool = 'substrate_tool'
        c9.position = loca.s_coater
        c9.set_output('coater_stage_vacuum', False)
        c9.set_output('substrate_tool', True)
        c9.move_axis('z', 0)
        c9.position = loca.substrate_rack_seq[0, 0]
        c9.set_output('substrate_tool', False)
        c9.move_axis('z', 0)
        c9.tool = None
        logging.info("Coated substrate returned to rack")
    except Exception as e:
        logging.error(f"Failed to return substrate to rack: {e}")
        raise

def return_vial_to_rack(vial_index, uncap_position):
    """
    Return the PEDOT:PSS vial to the rack and recap it.

    Args:
        vial_index (int): The index of the vial in the rack.
        uncap_position (tuple): The position for recapping the vial.

    Raises:
        Exception: If returning or recapping the vial fails.
    """
    try:
        c9.position = loca.clamp
        c9.set_output('gripper', True)
        c9.set_output('clamp', False)
        c9.move_axis('z', 0)
        c9.position = loca.vial_rack[vial_index]
        c9.set_output('gripper', False)
        c9.position = uncap_position
        c9.cap(pitch=1.75, revs=3.0, torque_thresh=1000, vel=5000, accel=5000)
        logging.info("PEDOT:PSS vial returned to rack and capped")
    except Exception as e:
        logging.error(f"Failed to return vial to rack: {e}")
        raise

def cleanup():
    """
    Perform cleanup operations after the coating process.

    Raises:
        Exception: If any cleanup step fails.
    """
    try:
        proc.remove_pipette(c9)
        t8.set_temp(1, 25)  # Reset temperature to room temperature
        c9.tool = None
        logging.info("Cleanup completed")
    except Exception as e:
        logging.error(f"Failed to complete cleanup: {e}")
        raise

def create_pedot_pss_film():
    """
    Main function to create a PEDOT:PSS film.

    This function orchestrates the entire process of creating a PEDOT:PSS film,
    including setup, coating, drying, and cleanup.
    """
    try:
        setup_coating_temperature(COATING_TEMPERATURE)
        pick_up_substrate()
        uncap_position = prepare_pedot_pss_solution()
        aspirate_and_dispense_solution()
        perform_blade_coating()

        logging.info(f"Allowing film to dry for {DRYING_TIME} seconds")
        time.sleep(DRYING_TIME)

        return_substrate_to_rack()
        vial_index = proc.find_rack_index('vial', 'polymer_A')
        return_vial_to_rack(vial_index, uncap_position)

        logging.info("PEDOT:PSS film creation process completed successfully")
    except Exception as e:
        logging.error(f"PEDOT:PSS film creation process failed: {e}")
    finally:
        cleanup()

if __name__ == "__main__":
    create_pedot_pss_film()
