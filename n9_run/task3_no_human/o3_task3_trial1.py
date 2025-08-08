# filename: fabricate_peng_film.py
"""
Fabricate a PEDOT:PSS (polymer_A) thin film with the best-performing
processing window extracted from PEDOT_PSS_manuscript.pdf.

Settings
--------
• Formulation          : pristine PEDOT:PSS (polymer_A, no additives)
• Substrate position   : (row 0, col 0) in the substrate rack
• Coating-stage temp   : 90 °C
• Blade speed          : 1 mm s⁻¹
• Dispense volume      : 0.30 mL (aspirate 0.50 mL for safety)
• Drying time on stage : 60 s
• Post-anneal          : 130 °C, 60 s
"""

import time                               # standard library (allowed)
import loca                               # location definitions
import pandas as pd                       # required import in template
import robotics as ro                     # robot API
from robotics import procedure as proc    # high-level helpers
import rack_status                        # rack inventory (required)

# ---------------------------------------------------------------------
# CONSTANTS (feel free to edit if needed)
COATING_TEMP_C      = 90      # °C  – stage temperature during coating
BLADE_SPEED_MM_S    = 1       # mm·s⁻¹
ASPIRATE_VOL_ML     = 0.50    # mL  – drawn from vial
DISPENSE_VOL_ML     = 0.30    # mL  – dropped on substrate
ANNEAL_TEMP_C       = 130     # °C
ANNEAL_TIME_S       = 60      # s
SUBSTRATE_IDX       = (0, 0)  # (row, col) in 12×6 substrate rack
VIAL_LABEL          = "polymer_A"
# ---------------------------------------------------------------------

def main() -> None:
    # -----------------------------------------------------------------
    # 0.  Verify polymer_A exists
    # -----------------------------------------------------------------
    if VIAL_LABEL not in ro.runtime['rack_status']['vial'].values:
        print("Experiment cannot be initiated.")
        return

    # -----------------------------------------------------------------
    # 1.  Initialise hardware handles
    # -----------------------------------------------------------------
    controller = ro.system.init('controller')   # robot arm (c9)
    heater     = ro.system.init('temperature')  # temperature controller (t8)
    coater     = ro.system.init('coater')       # blade-coating station

    # -----------------------------------------------------------------
    # 2.  Pick fresh substrate → place on coater stage
    # -----------------------------------------------------------------
    controller.tool = 'substrate_tool'
    controller.set_output('substrate_tool', True)                     # vacuum ON
    controller.position = loca.substrate_rack_seq[SUBSTRATE_IDX]      # above wafer
    controller.move_axis('z', controller.position[3] - 5000, vel=15000)
    time.sleep(0.3)
    controller.move_axis('z', controller.position[3] + 5000, vel=15000)
    controller.position = loca.s_coater                               # to stage
    controller.set_output('coater_stage_vacuum', True)                # hold wafer
    controller.set_output('substrate_tool', False)                    # release
    controller.tool = None                                            # drop tool

    # -----------------------------------------------------------------
    # 3.  Heat coating stage to 90 °C and stabilise
    # -----------------------------------------------------------------
    heater.set_temp(1, COATING_TEMP_C)                                # channel 1
    time.sleep(10)  # simple wait; replace with polling if available

    # -----------------------------------------------------------------
    # 4.  Fetch PEDOT:PSS vial, aspirate, dispense
    # -----------------------------------------------------------------
    vial_idx = proc.find_rack_index('vial', VIAL_LABEL)

    # pick vial
    controller.set_output('gripper', False)                           # open gripper
    controller.position = loca.vial_rack[vial_idx]
    controller.set_output('gripper', True)                            # grab vial
    controller.position = loca.clamp
    controller.set_output('clamp', False)                             # open clamp
    controller.set_output('clamp', True)                              # close clamp
    controller.set_output('gripper', False)                           # release

    # uncap
    uncap_pos = controller.uncap(pitch=1.75, revs=3.0, vel=5000, accel=5000)

    # new pipette → aspirate → dispense
    proc.new_pipette(controller)
    controller.position = loca.p_clamp
    controller.aspirate_ml(0, ASPIRATE_VOL_ML)
    controller.position = loca.p_coater
    controller.dispense_ml(0, DISPENSE_VOL_ML)
    proc.remove_pipette(controller)

    # recap vial and return
    controller.position = uncap_pos
    controller.cap(pitch=1.75, revs=3.0, torque_thresh=1000,
                   vel=5000, accel=5000)
    controller.set_output('clamp', False)
    controller.set_output('gripper', True)                            # grab vial
    controller.position = loca.vial_rack[vial_idx]
    controller.set_output('gripper', False)                           # drop vial

    # -----------------------------------------------------------------
    # 5.  Blade-coat the wet film
    # -----------------------------------------------------------------
    coater.velocity = BLADE_SPEED_MM_S
    coater.position = 45       # blade at start
    time.sleep(0.5)
    coater.position = 75       # sweep across
    time.sleep(1)

    # Dry for 60 s
    time.sleep(60)

    # -----------------------------------------------------------------
    # 6.  Post-anneal on the same hot stage (130 °C, 60 s)
    # -----------------------------------------------------------------
    heater.set_temp(1, ANNEAL_TEMP_C)
    time.sleep(ANNEAL_TIME_S)

    # -----------------------------------------------------------------
    # 7.  Cool stage back to 30 °C
    # -----------------------------------------------------------------
    heater.set_temp(1, 30)

    # -----------------------------------------------------------------
    # 8.  Return finished sample to rack
    # -----------------------------------------------------------------
    controller.tool = 'substrate_tool'
    controller.set_output('substrate_tool', True)
    controller.position = loca.s_coater
    controller.move_axis('z', controller.position[3] - 5000, vel=15000)
    time.sleep(0.3)
    controller.move_axis('z', controller.position[3] + 5000, vel=15000)
    controller.position = loca.substrate_rack_seq[SUBSTRATE_IDX]
    controller.set_output('substrate_tool', False)
    controller.tool = None
    controller.set_output('coater_stage_vacuum', False)

    # -----------------------------------------------------------------
    # 9.  Home the robot arm and finish
    # -----------------------------------------------------------------
    controller.position = [0, 0, 0, 0]   # home pose
    print("PEDOT:PSS thin film successfully fabricated.")


if __name__ == "__main__":
    main()