from typing import TypeVar

from . import mesh, options
import math
import numpy as np
from rivergen import options as op

DepthMap = TypeVar("DepthMap")

# Function to generate water depth according 
# to a flipped standard normal distribution
def depth_map(m: mesh.BaseSegment, var: float) -> DepthMap:
    """
    Generate a map of depths sampled from a
    flipped normal distribution centered around 
    the mid-index of m. 

    Args:
        m (mesh.MeshGrid): MeshGrid Segment
        var (float): Standard normal variance 

    Returns:
        DepthMap: DepthMap of same shape as m
    """
    out = []
    def _wd_gen(x,rnd1,rnd2):
        return op.MAX_DEPTH*math.exp(-5e-5*rnd1*(x+rnd2)**4)
    
    depth_linspace = np.linspace(-15,15,options.GP) 
    
    for i in range(len(m.yy)):
        r = []
        for j in range(options.GP):
            rnd1 = 0.7*math.sin(mesh.dtr(0.5*i)) + 1
            rnd2 = np.random.normal(2*np.sin(mesh.dtr(i)),var)
            r.append(_wd_gen(depth_linspace[j],rnd1,rnd2))
        out.append(r)
    
    return out