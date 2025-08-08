# filename: coat_pedot_pss.py
"""
Champion-recipe coating of PEDOT:PSS (polymer_A)
– Stage temperature : 90 °C
– Blade velocity     : 1 mm s-1
– Dispensed volume   : 0.20 mL
"""

# ---------------------------------------------------------------------------
# Mandatory imports for the N9 robotic system (from platform description)
# ---------------------------------------------------------------------------
import time
import loca                          # coordinate & rack maps
import pandas as pd                  # required by platform (even if unused here)
import robotics as ro                # Polybot core library
from robotics import procedure as proc
import rack_status                   # holds live rack maps

# ---------------------------------------------------------------------------
# Initialise hardware modules (same calls as in the platform example)
# ---------------------------------------------------------------------------
c9      = ro.system.init('controller')   # robot arm controller
t8      = ro.system.init('temperature')  # stage heater (channel 1)
coater  = ro.system.init('coater')       # blade-coating module

# ---------------------------------------------------------------------------
# Champion-recipe constants
# ---------------------------------------------------------------------------
T_COAT    = 90.0        # °C  – coating temperature
V_COAT    = 1.0         # mm s-1 – blade speed
VOL       = 0.20        # mL  – aspirate & dispense volume
SOL_LABEL = 'polymer_A' # PEDOT:PSS vial name

# ---------------------------------------------------------------------------
# Helper: wait until the stage reaches the target temperature (±2 °C)
# ---------------------------------------------------------------------------
def wait_for_stage(target=T_COAT, tol=2):
    while abs(t8.get_temp(1) - target) > tol:
        time.sleep(2)

# ---------------------------------------------------------------------------
# Main sequence
# ---------------------------------------------------------------------------
try:
    print('\n=== PEDOT:PSS champion-recipe coating START ===')

    # 1. Pick a fresh substrate and place it on the coater stage
    sub_idx = proc.find_rack_index('substrate', 'new')
    sub_pos = loca.substrate_rack_seq[sub_idx]
    print(f'> Substrate picked from rack index {sub_idx}')
    c9.tool = 'substrate_tool'
    c9.position = sub_pos
    c9.set_output('substrate_tool', True)          # vacuum ON – grip substrate
    c9.move_axis('z', c9.position[3] - 9000, vel=15000)
    c9.position = loca.s_coater
    c9.set_output('coater_stage_vacuum', True)     # hold on stage
    c9.set_output('substrate_tool', False)         # release substrate
    c9.tool = None
    print('  Substrate secured on coater stage.')

    # 2. Heat the stage to 90 °C
    print('> Heating stage to 90 °C …')
    t8.set_temp(1, T_COAT)
    wait_for_stage()
    print('  Stage at temperature.')

    # 3. Fetch PEDOT:PSS vial, place in clamp, and uncap
    vial_idx = proc.find_rack_index('vial', SOL_LABEL)
    vial_pos = loca.vial_rack[vial_idx]
    print(f'> Fetching {SOL_LABEL} (vial index {vial_idx})')
    c9.set_output('gripper', False)                # open gripper
    c9.position = vial_pos
    c9.set_output('gripper', True)                 # grip vial
    c9.move_axis('z', c9.position[3] - 5000, vel=15000)
    c9.position = loca.clamp
    c9.set_output('clamp', False)                  # open clamp
    c9.move_axis('z', c9.position[3] - 5000, vel=15000)
    c9.set_output('clamp', True)                   # close clamp (secure)
    c9.set_output('gripper', False)                # release vial
    c9.move_axis('z', c9.position[3] + 5000, vel=15000)
    c9.position = c9.uncap(pitch=1.75, revs=3.0, vel=5000, accel=5000)

    # 4. Pipette: aspirate & dispense 0.20 mL
    proc.new_pipette(c9)
    c9.position = loca.p_clamp
    c9.aspirate_ml(0, VOL)
    c9.position = loca.p_coater
    c9.dispense_ml(0, VOL)
    proc.remove_pipette(c9)
    print(f'  Dispensed {VOL} mL onto substrate.')

    # 5. Blade-coat the wet film
    coater.velocity = V_COAT
    coater.position = 45                          # blade start
    coater.position = 75                          # stroke across
    print('> Blade stroke complete – drying 60 s.')
    time.sleep(60)

    # 6. Re-cap vial & return to rack
    c9.position = loca.clamp
    c9.cap(pitch=1.75, revs=3.0, torque_thresh=1000,
           vel=5000, accel=5000)
    c9.set_output('clamp', False)                 # open clamp
    c9.set_output('gripper', True)                # grip vial
    c9.set_output('clamp', True)                  # close clamp (release)
    c9.move_axis('z', c9.position[3] - 5000, vel=15000)
    c9.position = vial_pos
    c9.set_output('gripper', False)               # drop vial
    print('  Vial returned & capped.')

    # 7. Return coated substrate to storage rack
    c9.tool = 'substrate_tool'
    c9.set_output('substrate_tool', True)
    c9.set_output('coater_stage_vacuum', False)
    c9.position = sub_pos
    c9.set_output('substrate_tool', False)
    c9.tool = None
    print('  Coated substrate stored back in rack.')

    print('=== Coating run FINISHED successfully ===')

finally:
    # Safety clean-up – ensure all outputs/heaters reset
    c9.set_output('substrate_tool', False)
    c9.set_output('coater_stage_vacuum', False)
    c9.set_output('gripper', False)
    t8.set_temp(1, 25)            # cool stage
    try:
        coater.position = 45      # park blade
    except Exception:
        pass