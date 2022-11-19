from config_avl import *


case_name = 'sciair001'

case = avl_case(case_name, 'full')

# HEADER
Mach = 0.0
Sref = 26
Cref = 1.98
Bref = 13.98
ref_point = [0., 0., 0.] # must be CG position if using AVL in trim mode

# WING
wing_loc = [0., 0., 0.]
wing_span = Bref
wing_taper = 0.4644
wing_root = 2.11
wing_sweep = 10.

wing_incidence = 0.
wing_root_af = '2414' # NACA
wing_tip_af = '2410'
wing_twist = -2.
wing_dihedral = 5.

# HTP
htp_loc = [6.13, 0., 1.14]
htp_span = 6
htp_taper = 0.49 #0.4644
htp_root = 1.6
htp_sweep = 20.

htp_incidence = -1.
htp_root_af = '0012' # NACA
htp_tip_af = '0012'
htp_twist = 0.
htp_dihedral = 0.

# ELEVATOR
elev_hinge = 0.7 # elevator hinge position as a fraction of the chord


# BUILDING THE CASE FILE

# HEADER
case.set_header(Mach, [Sref, Cref, Bref], ref_point)
# WING
case.set_wing_planform(
    wing_loc, wing_span, wing_taper, wing_root, wing_sweep)
case.set_wing_sections(wing_incidence, wing_root_af, wing_tip_af,
    wing_twist, wing_dihedral)
# HTP
case.set_htp_planform(
    htp_loc, htp_span, htp_taper, htp_root, htp_sweep)
case.set_htp_sections(htp_incidence, htp_root_af, htp_tip_af,
    htp_twist, htp_dihedral)
# ELEVATOR
case.set_elevator(elev_hinge)
    
case.write_case_file()
