import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from systems import ParticleMechanical, MultiParticle

np.random.seed(2025)


# STEPS_OF_SIMULATION = 10

NUMBER_OF_PARTICLES = 200
SURFACE_WIDTH = 10
SURFACE_HEIGHT = 10
DIMMENSION = 2
RADIUS = 4E-2

SAMPLING_TIME = 50E-5 # 6 when smaller box

SURFACE_PERIODIC = False

SIMULATION_NAME = "Particles on Torus" if SURFACE_PERIODIC else "Particles in Box"

FRAMES_NUMBER = 2400
DELAY_BETWEEN_FRAMES = 1/300 # in milliseconds

k_b = 1.380649E-23

PROTON_MASS = 1.66E-27 # kilograms
MASS_ZENON = 127 * PROTON_MASS # 127 ZENON
TEMPERATURE_ZENON_INIT = 298.15
SPEED_ZENON_AVG = np.sqrt(3/2*k_b*TEMPERATURE_ZENON_INIT*2/MASS_ZENON)

SPACING_BETWEEN_VALUES_IN_VELOCITIES_RANGE = 25



# systems initialisation
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

particles_velocities_range = np.arange(0, 500, SPACING_BETWEEN_VALUES_IN_VELOCITIES_RANGE)


# plotting

AVERAGING_NUMBER = 500 # how many frames are averaged for using in barchart (smooser)

scatter_size = 5

fig, (ax1, ax2) = plt.subplots(figsize=(5, 9), nrows=2)

# ax 1
ax1.set_xticks([]), ax1.set_yticks([])
ax1.set_aspect("equal")
ax1.set_xlim(-SURFACE_WIDTH/2, SURFACE_WIDTH/2)
ax1.set_ylim(-SURFACE_HEIGHT/2, SURFACE_HEIGHT/2)
ax1.set(xlabel=f"{SURFACE_WIDTH} meters", ylabel=f"{SURFACE_HEIGHT} meters")

scatter = ax1.scatter([], [], scatter_size)
temperature_txt = ax1.text(SURFACE_WIDTH/2*0.4, SURFACE_HEIGHT/2*0.92, s="")

# ax 2
ax2.set_xlim(particles_velocities_range[0], particles_velocities_range[-1])
ax2.set_ylim(0, NUMBER_OF_PARTICLES)
ax2.set(xlabel="Particle Speed [m/s]", ylabel="Number of Particles")

bar = ax2.bar(particles_velocities_range, 
              [0]*len(particles_velocities_range),
              width=0.9*np.gradient(particles_velocities_range),
              align="edge",
              alpha=0.8,
              label="Measured")


def maxwellian(velocities: np.ndarray, particles_number, system_temperature, particle_mass):
    maxwellian = (SPACING_BETWEEN_VALUES_IN_VELOCITIES_RANGE * 
                  particles_number * 
                  (particle_mass / (2 * np.pi * k_b * system_temperature))**(3/2) * 
                  4 * np.pi * velocities**2 * 
                  np.exp(-particle_mass * velocities**2 / (2 * k_b * system_temperature)))
    return maxwellian


maxwellian = ax2.plot(particles_velocities_range,
                      maxwellian(particles_velocities_range, 
                                 NUMBER_OF_PARTICLES, 
                                 multi_part.temperature_energy_average(), 
                                 MASS_ZENON),
                      color="orange",
                      label="Theoretical")
ax2.legend()
ax2.set_title("Maxwell–Boltzmann Distribution")

freqs_matrix = np.tile((np.histogram(multi_part.velocities(),
                                    bins=particles_velocities_range)[0].astype(float)),
                       (AVERAGING_NUMBER, 1))

def init_plot():
    scatter.set_offsets(multi_part.state)
    return (scatter, *bar.patches)
    
def update_plot(frame):
    multi_part.step()
    
    scatter.set_offsets(multi_part.state)
    scatter.set_color(multi_part.colors())
    
    temperature_txt.set_text(f"T={multi_part.temperature_energy_average():.2f} K")
    
    freqs, bins = np.histogram(multi_part.velocities(), bins=particles_velocities_range)
    
    freqs_matrix[frame % AVERAGING_NUMBER] = freqs
    freqs_mean = np.mean(freqs_matrix, axis=0)
    freqs_max = np.max(freqs_mean)
    
    for rect, height in zip(bar.patches, freqs):
        rect.set_height(height)
        
    if np.abs(freqs_max - ax2.get_ylim()[1]) > 10:
        ax2.set_ylim(0, ax2.get_ylim()[1] + (freqs_max - ax2.get_ylim()[1]))
        fig.canvas.draw()
        
    return (scatter, *bar.patches, temperature_txt)


animation = FuncAnimation(fig=fig, 
                          func=update_plot, 
                          frames=FRAMES_NUMBER, 
                          init_func=init_plot, 
                          blit=True, 
                          interval=DELAY_BETWEEN_FRAMES,
                          repeat=False,
                          save_count=FRAMES_NUMBER)

fig.suptitle(SIMULATION_NAME, fontsize=14) 

plt.show()


'''
https://www.youtube.com/watch?v=-0VRrnJx7u8

https://www.youtube.com/watch?v=PCkcYxsDVzs
'''



