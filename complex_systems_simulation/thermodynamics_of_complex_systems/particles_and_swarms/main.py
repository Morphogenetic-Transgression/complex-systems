import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from systems import ParticleMechanical, MultiParticle


# STEPS_OF_SIMULATION = 10

NUMBER_OF_PARTICLES = 30
SURFACE_WIDTH = 2
SURFACE_HEIGHT = 2

DIMMENSION = 2
RADIUS = 3E-2

SAMPLING_TIME = 0.02

SURFACE_PERIODIC = False

SIMULATION_NAME = "Particles on Torus" if SURFACE_PERIODIC else "Particles in Box"

FRAMES_NUMBER = 1200





particles_list = [ParticleMechanical(id = i,
                                     init_state = np.random.uniform(-SURFACE_WIDTH/2+RADIUS, 
                                                                    SURFACE_WIDTH/2-RADIUS, 
                                                                    (DIMMENSION,)), # np.array([0., (i-5)/10]),
                                     init_velocity = np.array([np.cos(np.pi/4), np.cos(np.pi/4)]),
                                     sampling_time = SAMPLING_TIME,
                                     mass = 1,
                                     radius = RADIUS) for i in range(NUMBER_OF_PARTICLES)]

particles_list[0].color = "red"
particles_list[0].set_velocity(np.array([-np.cos(np.pi/4), np.cos(np.pi/4)]))

multi_part = MultiParticle(particles_list, SURFACE_WIDTH, SURFACE_HEIGHT, SURFACE_PERIODIC)

particles_velocities_range = np.linspace(0, 2, 10)


# plotting
    
fig, (ax1, ax2) = plt.subplots(figsize=(5, 9), nrows=2)

ax1.set_xticks([]), ax1.set_yticks([])
ax1.set_aspect("equal")

scatter = ax1.scatter([], [])
bar = ax2.bar(particles_velocities_range, 
              [0]*len(particles_velocities_range),
              width=0.9*np.gradient(particles_velocities_range),
              align="edge",
              alpha=0.8)

def init_plot():
    ax1.set_xlim(-SURFACE_WIDTH/2, SURFACE_WIDTH/2)
    ax1.set_ylim(-SURFACE_HEIGHT/2, SURFACE_HEIGHT/2)
    scatter.set_offsets(multi_part.state)
    ax2.set_xlim(particles_velocities_range[0], particles_velocities_range[-1])
    ax2.set_ylim(0, NUMBER_OF_PARTICLES)
    ax2.set(xlabel="Particle Speed [m/s]", ylabel="Number of Particles")
    return (scatter, *bar.patches)
    
def update_plot(frame):
    multi_part.step()
    
    scatter.set_offsets(multi_part.state)
    scatter.set_color(multi_part.colors())
    
    freqs, bins = np.histogram(multi_part.velocities(), bins=particles_velocities_range)
    for rect, height in zip(bar.patches, freqs):
        rect.set_height(height)
        
    return (scatter, *bar.patches)


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
https://www.youtube.com/watch?v=-0VRrnJx7u8

https://www.youtube.com/watch?v=PCkcYxsDVzs
'''



