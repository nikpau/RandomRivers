# Breadth and spacing of segments
GP = 76 #  No. of grid points per segment width
BPD = 20 # distance between gridpoints [m]

L_RANGE = (400,2000) # Range for straight segments [m] (ξ)
R_RANGE = (500,2000) # Range of circle radii [m] (r)
ANG_RANGE = (60,80) # Range of angles along the circles [deg] (ϕ)
MAX_DEPTH = 7 # River depth at deepest point [m] (κ)
MAX_VEL = 1 # Maximum current velocity [ms⁻¹] (ν)

# Print information about the generation 
# process to stdout
VERBOSE: bool = True