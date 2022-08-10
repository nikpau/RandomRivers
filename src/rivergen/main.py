import itertools
import os
import sys
import threading
import time
import numpy as np
from rivergen import mesh, depth, currents
from datetime import datetime
from typing import Generator, Tuple

def merge_coords(m: mesh.Segment) -> Generator[Tuple, None, None]:
    """Merge coordinate mesh into a generator for further processing.
    """
    mx = np.hstack(m.xx)
    my = np.hstack(m.yy)

    if not mx.shape == my.shape:
        raise ValueError("Shapes of mesh, depth map and current map do not match.")

    return zip(mx,my)

def merge_metrics(d: depth.DepthMap,c: currents.CurrentMap) -> Generator[Tuple, None, None]:
    """Merge depth map and current map into a generator for further processing.
    """
    d = np.hstack(d)
    cx = np.hstack(c.x)
    cy = np.hstack(c.y)
    cvel = np.sqrt(cx**2 + cy**2)
    zeros = np.zeros_like(cx)

    l = [d,cx,cy,cvel,zeros]

    if not all(map(lambda x: x.shape == l[0].shape,l)):
        raise ValueError("Shapes of depth map and current maps do not match.")
    
    return zip(zeros,cy,cx,d,zeros,zeros,cvel)

def write_to_file(
    coords: Generator[Tuple, None, None],
    metrics: Generator[Tuple, None, None],
    folder_name: os.PathLike) -> None:
    """Write to file.
    """
    with open(f"{folder_name}/coords.txt", "w") as f:
        for coord in coords:
            f.write("{} {}\n".format(*coord))

    with open(f"{folder_name}/metrics.txt", "w") as f:
        for metric in metrics:
            f.write("{} {} {} {} {} {} {}\n".format(*metric))

def build(segments: int, var: float, vel: float) -> os.PathLike:
    """
    Package main function. Generates xy 
    coordinates, depths and current fields
    from randomly sized curves and lines. 
    Saves the output as whitespace separated 
    .txt file in a folder named by execution time of
    the script.
    
    The files containing coordinates (coords.txt)
    have two columns [x,y].
    (metrics.txt) has seven colums 
    [_, current_vel_y,current_vel_x,water_depth, _, _, current_velocity]
    
    This format is currently very specific. In order to change it
    see the `merge_metrics()` function

    Args:
        segments (int): Number of segments making up the river/road
        var (float): Variability of depth distribution
        vel (float): maximum current velocity

    Returns:
        os.PathLike: path to folder containing generated files
    """

    parent = "gen"
    
    # Check if `gen` folder exists. If not, create it.
    if not os.path.isdir(parent):
        os.mkdir(parent)

    # Create folder
    folder_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = f"{parent}/{folder_name}"
    os.mkdir(filepath)

    # Generate mesh
    m = mesh.generate(segments,f"{parent}/{folder_name}/Segments")
    print("Mesh generated.")

    # Generate depth map
    d = depth.depth_map(m,var=var)
    print("Depth map generated.")

    # Generate current map
    c = currents.current_map(m,v=vel)
    print("Current map generated.")

    # Merge coordinates and metrics
    coords = merge_coords(m)
    metrics = merge_metrics(d,c)
    print("Merged.")

    # Loading animation, beause why not?
    done = False
    def animate():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\rWriting to file... ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\nDone!')
    t = threading.Thread(target=animate)
    t.start()

    # Write to file
    write_to_file(coords,metrics,filepath)

    done = True

    return filepath