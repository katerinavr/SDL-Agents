# filename: make_PEDOT_PSS_film.py
import time
import pandas as pd
import robotics as ro
from robotics import procedure as proc
import loca
import rack_status   # brings ro.runtime['rack_status'] into scope

# ---------------- Champion processing parameters (from PEDOT_PSS_manuscript.pdf) ----------
CHAMPION_TEMP_COAT = 90        # °C – substrate temperature during coating
CHAMPION_SPEED_COAT = 1        # mm s-1 – blade velocity
CHAMPION_TEMP_POST = 60        # °C – post-treatment shearing temperature
CHAMPION_SPEED_POST = 1        # mm s-1 – post-treatment shear speed
CHAMPION_ANNEAL_TEMP = 130     # °C – final anneal
CHAMPION_ANNEAL_TIME = 60      # s  – final anneal dwell
VOLUME_ASPIRATE_ML = 0.50      # mL – total solution pulled
VOLUME_DISPENSE_ML = 0.20      # mL – solution dispensed onto substrate
POLYMER_LABEL = 'polymer_A'    # PEDOT:PSS (5 vol % EG)

# ---------------- Initialise hardware -----------------------------------------------------
c9 = ro.system.init('controller')
t8 = ro.system.init('temperature')
coater = ro.system.init('coater')

# ---------------- Helper: find rack indices ------------------------------------------------
vial_index = proc.find_rack_index('vial', POLYMER_LABEL)
substrate_index = (0, 0)  # choose first “new” substrate

# ---------------- STEP 1 – pick up and place a fresh substrate -----------------------------
c9.tool = 'substrate_tool'                          # pick Bernoulli gripper
c9.set_output('substrate_tool', True)               # vacuum ON
c9.position = loca.substrate_rack_seq[substrate_index]
c9.move_axis('z', c9.position[3] - 3000, vel=15000) # approach substrate
c9.move_axis('z', 0)                                # lift substrate
c9.position = loca.s_coater                         # move to coater stage
c9.set_output('coater_stage_vacuum', True)          # hold substrate on stage
c9.set_output('substrate_tool', False)              # release substrate
c9.tool = None                                      # park Bernoulli gripper

# ---------------- STEP 2 – bring the PEDOT:PSS vial to the clamp ---------------------------
c9.position = loca.vial_rack[vial_index]            # go to polymer vial
c9.set_output('gripper', False)                     # open gripper
c9.move_axis('z', c9.position[3] - 3000, vel=8000)  # lower on vial
c9.set_output('gripper', True)                      # grip vial
c9.move_axis('z', 0)                                # lift vial
c9.position = loca.clamp                            # move to clamp
c9.set_output('clamp', False)                       # open clamp
c9.position = loca.clamp                            # insert vial
c9.set_output('clamp', True)                        # close clamp
c9.set_output('gripper', False)                     # release vial
c9.uncap(pitch=1.75, revs=3.0, vel=5000, accel=5000)  # uncap and leave cap on gripper
c9.move_axis('z', 0)                                # retract

# ---------------- STEP 3 – pipette champion solution --------------------------------------
proc.new_pipette(c9)                                # mount fresh pipette
c9.position = loca.p_clamp                          # dip pipette into vial
c9.aspirate_ml(0, VOLUME_ASPIRATE_ML)               # aspirate solution

# ---------------- STEP 4 – dispense on substrate at coater --------------------------------
t8.set_temp(1, CHAMPION_TEMP_COAT)                  # set coating temp = 90 °C
c9.position = loca.p_coater                         # above substrate
c9.dispense_ml(0, VOLUME_DISPENSE_ML)               # drop 0.20 mL
proc.remove_pipette(c9)                             # discard pipette

# ---------------- STEP 5 – blade coat the film --------------------------------------------
coater.velocity = CHAMPION_SPEED_COAT               # 1 mm s-1
coater.position = 45                                # blade start
coater.position = 75                                # blade sweep
time.sleep(3)                                       # allow film to level/dry

# ---------------- OPTIONAL STEP 6 – post-treatment ----------------------------------------
# If MeOH/EtOH (40/60 v %) vial is present in rack, uncomment block below.
"""
post_solvent_label = 'MeOH_EtOH_40_60'
post_vial_index = proc.find_rack_index('vial', post_solvent_label)
c9.position = loca.vial_rack[post_vial_index]
c9.set_output('gripper', True); c9.move_axis('z', 0)
c9.position = loca.clamp
c9.set_output('clamp', False); c9.set_output('clamp', True); c9.set_output('gripper', False)
c9.uncap(pitch=1.75, revs=3.0, vel=5000, accel=5000)
proc.new_pipette(c9)
c9.position = loca.p_clamp; c9.aspirate_ml(0, VOLUME_ASPIRATE_ML)
t8.set_temp(1, CHAMPION_TEMP_POST)                  # 60 °C
c9.position = loca.p_coater; c9.dispense_ml(0, VOLUME_DISPENSE_ML)
proc.remove_pipette(c9)
coater.velocity = CHAMPION_SPEED_POST; coater.position = 45; coater.position = 75
time.sleep(2)
"""

# ---------------- STEP 7 – final anneal ----------------------------------------------------
t8.set_temp(1, CHAMPION_ANNEAL_TEMP)                # 130 °C
time.sleep(CHAMPION_ANNEAL_TIME)                    # dwell 60 s

# ---------------- STEP 8 – return substrate & clean-up ------------------------------------
t8.set_temp(1, 25)                                  # cool down stage
coater.position = 45                                # park blade
c9.tool = 'substrate_tool'
c9.set_output('substrate_tool', True)
c9.set_output('coater_stage_vacuum', False)         # release from stage
c9.move_axis('z', c9.position[3] - 3000, vel=15000)
c9.move_axis('z', 0)
c9.position = loca.substrate_rack_seq[substrate_index]  # back to rack
c9.set_output('substrate_tool', False)
c9.tool = None

# ---------------- STEP 9 – recap vial & shutdown ------------------------------------------
c9.position = loca.clamp
c9.cap(pitch=1.75, revs=3.0, torque_thresh=1000, vel=5000, accel=5000)
c9.set_output('clamp', False)                       # open clamp
c9.set_output('gripper', True)                      # grab vial
c9.position = loca.vial_rack[vial_index]            # return vial
c9.set_output('gripper', False)
c9.position = [0, 0, 0, 0]                          # home
print("Champion PEDOT:PSS film fabricated successfully.")