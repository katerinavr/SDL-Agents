# filename: coat_pedot_pss.py
"""
Champion-recipe PEDOT:PSS (polymer_A) thin-film coating
– Stage temperature : 90 °C
– Blade velocity     : 1 mm s-1
– Dispensed volume   : 0.20 mL
"""

import time
import loca
import robotics as ro
from robotics import procedure as proc

# --------------------------------------------------------------
# hardware handles (as in the platform description)
# --------------------------------------------------------------
c9      = ro.system.init('controller')     # robot arm
t8      = ro.system.init('temperature')    # stage heater
coater  = ro.system.init('coater')         # blade-coater

# ------------------------------ recipe constants --------------
T_COAT    = 90.0        # °C
V_COAT    = 1.0         # mm s-1
VOL       = 0.20        # mL – aspirate and dispense
SOL_LABEL = 'polymer_A' # PEDOT:PSS vial name
# --------------------------------------------------------------

def wait_for_stage(target=T_COAT, tol=2, poll=2):
    """Wait until the stage temperature is within ±tol of target."""
    while abs(t8.get_temp(1) - target) > tol:
        time.sleep(poll)

try:
    run_id = ro.log_run({       # ELN entry – traceability
        'material'      : 'PEDOT:PSS',
        'EG_vol%'       : 5,
        'stage_T(°C)'   : T_COAT,
        'blade_speed'   : V_COAT,
        'script'        : __file__
    })
    print(f'\n=== PEDOT:PSS champion-recipe coating (run {run_id}) ===')

    # 1. pick a fresh substrate
    sub_idx = proc.find_rack_index('substrate', 'new')
    sub_pos = loca.substrate_rack_seq[sub_idx]
    print(f'> Substrate index {sub_idx}')
    c9.tool = 'substrate_tool'
    c9.position = sub_pos
    c9.set_output('substrate_tool', True)     # pick
    c9.move_axis('z', c9.position[3]-9000, vel=15000)
    c9.position = loca.s_coater
    c9.set_output('coater_stage_vacuum', True)
    c9.set_output('substrate_tool', False)    # release
    c9.tool = None
    print('  Substrate on coater stage')

    # 2. heat stage
    t8.set_temp(1, T_COAT)
    print('> Heating stage …')
    wait_for_stage()
    print('  Stage ready')

    # 3. bring polymer_A to clamp & uncap
    vial_idx = proc.find_rack_index('vial', SOL_LABEL)
    vial_pos = loca.vial_rack[vial_idx]
    print(f'> Vial index {vial_idx}')
    c9.set_output('gripper', False)
    c9.position = vial_pos
    c9.set_output('gripper', True)            # grip vial
    c9.move_axis('z', c9.position[3]-5000, vel=15000)
    c9.position = loca.clamp
    c9.set_output('clamp', False)
    c9.move_axis('z', c9.position[3]-5000, vel=15000)
    c9.set_output('clamp', True)             # secure vial
    c9.set_output('gripper', False)
    c9.move_axis('z', c9.position[3]+5000, vel=15000)
    c9.position = c9.uncap(pitch=1.75, revs=3.0,
                           vel=5000, accel=5000)

    # 4. pipette – aspirate & dispense
    proc.new_pipette(c9)
    c9.position = loca.p_clamp
    c9.aspirate_ml(0, VOL)
    c9.position = loca.p_coater
    c9.dispense_ml(0, VOL)
    proc.remove_pipette(c9)
    print(f'  Dispensed {VOL} mL')

    # 5. blade-coat
    coater.velocity  = V_COAT
    coater.position  = 45       # start
    coater.position  = 75       # stroke
    print('> Blade stroke done – drying 60 s')
    time.sleep(60)

    # 6. recap & return vial
    c9.position = loca.clamp
    c9.cap(pitch=1.75, revs=3.0,
           torque_thresh=1000, vel=5000, accel=5000)
    c9.set_output('clamp', False)
    c9.set_output('gripper', True)
    c9.set_output('clamp', True)
    c9.move_axis('z', c9.position[3]-5000, vel=15000)
    c9.position = vial_pos
    c9.set_output('gripper', False)
    print('  Vial returned')

    # 7. store coated substrate
    c9.tool = 'substrate_tool'
    c9.set_output('substrate_tool', True)
    c9.set_output('coater_stage_vacuum', False)
    c9.position = sub_pos
    c9.set_output('substrate_tool', False)
    c9.tool = None
    print('  Coated substrate stored')

    print('=== Coating run FINISHED ===')

finally:
    # ensure all actuators off & blade parked
    c9.set_output('substrate_tool', False)
    c9.set_output('coater_stage_vacuum', False)
    c9.set_output('gripper', False)
    t8.set_temp(1, 25)          # cool stage
    coater.position = 45        # park blade