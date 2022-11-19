from math import cos, tan, pi
import datetime


# aerfoil : detec "xxxx" => NACA, else : file
# what if write_case_file is called before having set the geometry?
# => Error

class avl_case:
    
    def __init__(self, name: str, geom_type: str):
        """ geom type : 'wing', 'full' (wing+tail)"""
        self._name = name
        self._geom_type = geom_type
        self._has_wing = 0
        self._has_htp = 0
        self._has_elevator = 0
        
    def set_header(self, mach, ref_dimensions, ref_point):
        """ ref_dimensons = [Sref, Cref, Bref]
            ref_point = [X_ref, Y_ref, Z_ref] = moment ref point
            cdp : profile drag coeff """
        self._mach = mach
        self._ref_dimensions = ref_dimensions
        self._ref_point = ref_point
        #self._cdp = cdp
    
    def set_wing_planform(self, loc, span, taper, root, sweep):
        self._has_wing += 0.5
        """ wing root LE point location,
            wingspan, taper ratio, root chord, leading edge sweep angle """
        self._wing_location = loc
        self._wing_span = span
        self._wing_taper = taper
        self._wing_root = root
        self._wing_sweep = sweep
    
    def set_wing_sections(self, incidence, root_af, tip_af, 
        twist, dihedral):
        self._has_wing += 0.5
        """ incidence setting angle, root aerofoil, tip aerofoil
            tip twist angle """
        self._wing_incidence = incidence
        self._wing_root_af = root_af
        self._wing_tip_af = tip_af
        self._wing_twist = twist
        self._wing_dihedral = dihedral

    def set_htp_planform(self, loc, span, taper, root, sweep):
        """ htp root LE point location,
            wingspan, taper ratio, root chord, leading edge sweep angle """
        self._has_htp +=0.5
        
        self._htp_location = loc
        self._htp_span = span
        self._htp_taper = taper
        self._htp_root = root
        self._htp_sweep = sweep
    
    def set_htp_sections(self, incidence, root_af: str, tip_af: str, 
        twist, dihedral):
        """ incidence setting angle, root aerofoil, tip aerofoil
            tip twist angle """
        
        self._has_htp +=0.5
        
        self._htp_incidence = incidence
        self._htp_root_af = root_af
        self._htp_tip_af = tip_af
        self._htp_twist = twist
        self._htp_dihedral = dihedral

    def set_elevator(self, elev_hinge):
        self._has_elevator = 1
        self._elev_hinge = elev_hinge
        
    def _write_header(self):
        with open(self._name + '.avl', 'w') as file:
            header_now = datetime.datetime.now()
            header_line = '# Case file generated on ' + str(header_now)
            file.write(header_line + '\n\n')
            # HEADER
            file.write(self._name + '\n')
            # mach
            file.write(str(self._mach))
            file.write('\t\t!   Mach\n')
            # symmetry planes
            file.write('0.0 0.0 0.0')
            file.write('\t\t!   iYsym  iZsym  Zsym\n')
            # reference dimensions
            [Sref, Cref, Bref] = [str(i) for i in self._ref_dimensions]
            file.write(Sref + ' ' + Cref + ' ' + Bref)
            file.write('\t\t!   Sref   Cref   Bref\n')
            # moments reference point
            [Xref, Yref, Zref] = [str(i) for i in self._ref_point]
            file.write(Xref + ' ' + Yref + ' ' + Zref)
            file.write('\t\t!   Xref   Yref   Zref\n')
            # profile drage coeff
            file.write('0.0')
            file.write('\t\t!   CDp\n')
    
    def _write_wing(self):
        if self._has_wing != 1:
            print('\n\t/!\ Wing parameters have not correctly been set !')
            print('\t\t=> Wing not included in the case file\n')
            return
        
        with open(self._name + '.avl', 'a') as file:
            file.write('\n' + '#'*15 + ' WING ' + '#'*15 + '\n')
            # WING
            file.write('SURFACE\nWing\n')
            # chordwise and spanwise panelling
            file.write('10  1.0  22  1.0')
            file.write('\t! Nchord   Cspace   Nspan  Sspace\n')
            # duplicatig at y=0
            file.write('YDUPLICATE\n0.0\n')
            # wing setting angle
            file.write('ANGLE\n'+str(self._wing_incidence)+'\n')
            # wing root LE positon
            file.write('TRANSLATE\n')
            for x in self._wing_location:
                file.write(str(x)+' ')
            file.write('\n')
            
            
            file.write('\n#Xle  Yle  Zle  chord  angle\n')
            # ROOT
            file.write('SECTION  ! ROOT\n')
            # LE location, root chord,
            # and angle relative to incidence angle
            #for x in self._wing_location:
            #    file.write(str(x)+' ')
            file.write('0.0 0.0 0.0 ')
            file.write(str(self._wing_root) + ' 0.0\n')
            # aerofoil
            file.write('NACA\n' + self._wing_root_af + '\n')
            
            
            # TIP
            file.write('\nSECTION  ! TIP\n')
            # LE location, root chord,
            # and angle relative to incidence angle
            tip_le_x = self._wing_span/2*tan(pi/180*self._wing_sweep)
            tip_le_y = self._wing_span/2*cos(pi/180*self._wing_sweep)
            tip_le_z = self._wing_span/2*tan(pi/180*self._wing_dihedral)
            file.write('{:.3f}'.format(tip_le_x) + ' ')
            file.write('{:.3f}'.format(tip_le_y) + ' ')
            file.write('{:.3f}'.format(tip_le_z) + ' ')
            tip_chord = self._wing_root*self._wing_taper
            file.write('{:.3f}'.format(tip_chord) + ' ')
            file.write(str(self._wing_twist) + '\n')
            # aerofoil
            file.write('NACA\n' + self._wing_tip_af + '\n')
            

    def _write_htp(self):        
        if self._has_htp != 1:
            print('\n\t/!\ HTP parameters have not correctly been set !')
            print('\t\t=> HTP not included in the case file\n')
            return
        
        with open(self._name + '.avl', 'a') as file:
            file.write('\n' + '#'*15 + ' HTP ' + '#'*15 + '\n')
            # HORIZONTAL TAILPLANE
            file.write('SURFACE\nHorizontalTailplane\n')
            # chordwise and spanwise panelling
            file.write('10  1.0  22  1.0')
            file.write('\t! Nchord   Cspace   Nspan  Sspace\n')
            # duplicatig at y=0
            file.write('YDUPLICATE\n0.0\n')
            # wing setting angle
            file.write('ANGLE\n'+str(self._htp_incidence)+'\n')
            # wing root LE positon
            file.write('TRANSLATE\n')
            for x in self._htp_location:
                file.write(str(x)+' ')
            file.write('\n')
            
            
            file.write('\n#Xle  Yle  Zle  chord  angle\n')
            # ROOT
            file.write('SECTION  ! ROOT\n')
            # LE location, root chord,
            # and setting angle relative to htp incidence angle (=0)
            #for x in self._htp_location:
            #    file.write(str(x)+' ')
            file.write('0.0 0.0 0.0 ')
            file.write(str(self._htp_root) + ' 0.0\n')
            # aerofoil
            file.write('NACA\n' + self._htp_root_af + '\n')
            # control
            if self._has_elevator==1:
                file.write('#Cname Cgain Xhinge HingeVec SgnDup\n')
                file.write('CONTROL\nelevator 1.0 ')
                file.write(str(self._elev_hinge)+'  0.0 0.0 0.0  1.0\n')
            
            # TIP
            file.write('\nSECTION  ! TIP\n')
            # LE location, root chord,
            # and angle relative to incidence angle
            tip_le_x = self._htp_span/2*tan(pi/180*self._htp_sweep)
            tip_le_y = self._htp_span/2*cos(pi/180*self._htp_sweep)
            tip_le_z = self._htp_span/2*tan(pi/180*self._htp_dihedral)
            file.write('{:.3f}'.format(tip_le_x) + ' ')
            file.write('{:.3f}'.format(tip_le_y) + ' ')
            file.write('{:.3f}'.format(tip_le_z) + ' ')
            tip_chord = self._htp_root*self._htp_taper
            file.write('{:.3f}'.format(tip_chord) + ' ')
            file.write(str(self._htp_twist) + '\n')
            # aerofoil
            file.write('NACA\n' + self._htp_tip_af + '\n')
            # control
            if self._has_elevator==1:
                file.write('#Cname Cgain Xhinge HingeVec SgnDup\n')
                file.write('CONTROL\nelevator 1.0 ')
                file.write(str(self._elev_hinge)+'  0.0 0.0 0.0  1.0\n')

    def write_case_file(self):
        self._write_header()
        self._write_wing()
        if self._geom_type == 'full':
                # self._write_vtp()
                self._write_htp()
        print('\tCase file written as ' + self._name + '.avl')

