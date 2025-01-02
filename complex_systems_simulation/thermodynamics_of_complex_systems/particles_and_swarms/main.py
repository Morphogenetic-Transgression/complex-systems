import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from systems import ParticleMechanical, MultiParticle


# STEPS_OF_SIMULATION = 10

NUMBER_OF_PARTICLES = 20
SURFACE_WIDTH = 2
SURFACE_HEIGHT = 2

DIMMENSION = 2
RADIUS = 4E-2

SAMPLING_TIME = 0.02

SURFACE_PERIODIC = False

SIMULATION_NAME = "Particles on Torus" if SURFACE_PERIODIC else "Particles in Box"

FRAMES_NUMBER = 1200





particles_list = [ParticleMechanical(id = i,
                                     init_state = np.random.uniform(-SURFACE_WIDTH/2+RADIUS, 
                                                                    SURFACE_WIDTH/2-RADIUS, 
                                                                    (DIMMENSION,)), # np.array([0., (i-5)/10]),
                                     init_velocity = np.array([1, 1]),
                                     sampling_time = SAMPLING_TIME,
                                     mass = 1,
                                     radius = RADIUS) for i in range(NUMBER_OF_PARTICLES)]

particles_list[0].color = "red"
particles_list[0].set_velocity(np.array([-1, 1/2]))

multi_part = MultiParticle(particles_list, SURFACE_WIDTH, SURFACE_HEIGHT, SURFACE_PERIODIC)


# plotting
    
fig, ax = plt.subplots()

ax.set_xlim(-SURFACE_WIDTH/2, SURFACE_WIDTH/2)
ax.set_ylim(-SURFACE_HEIGHT/2, SURFACE_HEIGHT/2)

scatter = ax.scatter([], [])
# scat = ax.scatter(t[0], z[0], c="b", s=5, label=f'v0 = {v0} m/s')
# ax.set(xlim=[0, 3], ylim=[-4, 10], xlabel='Time [s]', ylabel='Z [m]')
# ax.legend()

def init_plot():
    scatter.set_offsets(multi_part.state)
    return scatter,
    
def update_plot(frame):
    multi_part.step()
    scatter.set_offsets(multi_part.state)
    scatter.set_color(multi_part.colors())
    return scatter,


animation = FuncAnimation(fig=fig, 
                          func=update_plot, 
                          frames=FRAMES_NUMBER, 
                          init_func=init_plot, 
                          blit=True, 
                          interval=30,
                          repeat=False,
                          save_count=FRAMES_NUMBER)

fig.suptitle(SIMULATION_NAME, fontsize=14) 

plt.show()


'''
https://thermotools.github.io/thermopack/v2.1.0/home.html

https://gistlib.com/python/create-a-thermodynamic-simulation-in-python

https://phaseslab.com/pycalphad/

https://alphapedia.ru/w/Torus

https://www.geeksforgeeks.org/rendering-3d-surfaces-using-parametric-equations-in-python/

https://scipython.com/book/chapter-7-matplotlib/examples/a-torus/

https://geometry.docs.pyansys.com/version/stable/examples/03_modeling/surface_bodies.html

https://plotly.com/python/3d-surface-plots/

https://stackoverflow.com/questions/51613756/drawing-animation-on-torus-with-python

https://scipython.com/blog/diffusion-on-the-surface-of-a-torus/

https://yangyushi.github.io/science/2020/11/02/pbc_py.html

https://groups.csail.mit.edu/mac/projects/amorphous/GrayScott/


'''

