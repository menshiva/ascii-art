# Run this scipt to have a visual check how the simulation is behaving

from collections import namedtuple

import numpy as np
from IPython.display import HTML
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import rc

import space_motion

def visualize_results(simulation, timestamp, xlim, ylim, *space_objects):
    colors = [o.color for o in space_objects]
    x = [o.x for o in space_objects]
    y = [o.y for o in space_objects]

    fig = plt.figure(figsize=(15, 15))
    plt.xlim(xlim) 
    plt.ylim(ylim) 
    scat = plt.scatter(x, y, c=colors, s=100)

    def update_plot(simulation, _, scat):
        scat.set_offsets([list(o) for o in simulation.values()])
        return scat,
    
    interval = timestamp*1000
    ani = animation.FuncAnimation(fig, update_plot, frames=list(simulation),
                                  fargs=(None, scat), interval=interval, repeat=False)

    return ani


def main():
    
    SpaceObject = namedtuple('SpaceObject', 'name mass x y vx vy color')
    
    # Define universal gravitation constant
    G=6.67408e-11 #N-m2/kg2

    #Reference quantities
    m_sun=1.989e30 #mass of the sun [kg]
    m_earth = 5.972e24 #mass of the earth [kg]

    au = 1.495e11 #astronomical unit, approximately distance from earth to sun [m]
    speed_earth = 30.0e3 #speed of earth (relative to sun) [m/s]
    
    mass_venus = 4.867e24
    speed_venus = 35.02e3 #[m/s]
    distance_venus = 108.21e9 #[m]

    day = 24*3600 #[s]
    
    sun = SpaceObject(name='sun', mass=1*m_sun, x=0.0, y=0.0, vx=0.0, vy=0.0, color='yellow')
    earth = SpaceObject(name='earth', mass=1*m_earth, x=au, y=0.0, vx=0.0, vy=speed_earth, color='blue')
    venus = SpaceObject(name='venus', mass=mass_venus, x=-distance_venus, y=0.0, vx=0.0, vy=-speed_venus,
                    color='orange')

    simulation = space_motion.simulate_motion(0.5*day, 800, sun, earth, venus)
    
    ani = visualize_results(simulation, 0.2, (-2*au, 2*au), (-2*au, 2*au), sun, earth, venus)
    plt.show()
    HTML(ani.to_jshtml())
    

if __name__ == '__main__':
    main()
