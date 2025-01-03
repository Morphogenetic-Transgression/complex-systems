import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from systems import ParticleMechanical, MultiParticle

np.random.seed(2025)


# STEPS_OF_SIMULATION = 10

NUMBER_OF_PARTICLES = 30
SURFACE_WIDTH = 2
SURFACE_HEIGHT = 2

DIMMENSION = 2
RADIUS = 2E-2

SAMPLING_TIME = 50E-6

SURFACE_PERIODIC = False

SIMULATION_NAME = "Particles on Torus" if SURFACE_PERIODIC else "Particles in Box"

FRAMES_NUMBER = 2400

k_b = 1.380649E-23

MASS_ZENON = 127*1.66E-27
TEMPERATURE_ZENON_INIT = 293.15
SPEED_ZENON_AVG = np.sqrt(3/2*k_b*TEMPERATURE_ZENON_INIT*2/MASS_ZENON)




particles_list = [ParticleMechanical(id = i,
                                     init_state = np.random.uniform(-SURFACE_WIDTH/2+RADIUS, 
                                                                    SURFACE_WIDTH/2-RADIUS, 
                                                                    (DIMMENSION,)), # np.array([0., (i-5)/10]),
                                     init_velocity = SPEED_ZENON_AVG * np.array([np.cos(np.pi/4), np.cos(np.pi/4)]),
                                     sampling_time = SAMPLING_TIME,
                                     mass = MASS_ZENON,
                                     radius = RADIUS) for i in range(NUMBER_OF_PARTICLES)]

particles_list[0].color = "red"
particles_list[0].set_velocity(SPEED_ZENON_AVG * np.array([np.cos(np.pi/4), np.cos(np.pi/4)]))

multi_part = MultiParticle(particles_list, SURFACE_WIDTH, SURFACE_HEIGHT, SURFACE_PERIODIC)

particles_velocities_range = np.linspace(0, 500, 10)


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

temperature_txt = ax1.text(SURFACE_WIDTH/2*0.4, SURFACE_HEIGHT/2*0.92, s="")

maxwellian = ...

# freqs_matrix = ...

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
        
    temperature_txt.set_text(f"T={multi_part.temperature_theoretical():.2f} K")
        
    return (scatter, *bar.patches, temperature_txt)


animation = FuncAnimation(fig=fig, 
                          func=update_plot, 
                          frames=FRAMES_NUMBER, 
                          init_func=init_plot, 
                          blit=True, 
                          interval=1/30,
                          repeat=False,
                          save_count=FRAMES_NUMBER)

fig.suptitle(SIMULATION_NAME, fontsize=14) 

plt.show()


'''
https://www.youtube.com/watch?v=-0VRrnJx7u8

https://www.youtube.com/watch?v=PCkcYxsDVzs
'''



