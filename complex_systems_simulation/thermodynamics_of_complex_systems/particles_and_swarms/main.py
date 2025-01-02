import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from systems import ParticleMechanical, MultiParticle


SIMULATION_NAME = 'Particles in Box'
VIDEO_DURATION = 20
FRAMES_NUMBER = 1200
STEPS_OF_SIMULATION = 10
NUMBER_OF_PARTICLES = 20
SAMPLING_TIME = 0.02
SURFACE_WIDTH = 2
SURFACE_HEIGHT = 2
DIMMENSION = 2
RADIUS = 4E-2


particles_list = [ParticleMechanical(id = i,
                                     init_state = np.random.uniform(-SURFACE_WIDTH/2+RADIUS, 
                                                                    SURFACE_WIDTH/2-RADIUS, 
                                                                    (DIMMENSION,)), # np.array([0., (i-5)/10]),
                                     init_velocity = np.array([np.cos(np.pi/4), np.cos(np.pi/4)]),
                                     sampling_time = SAMPLING_TIME,
                                     mass = 1,
                                     radius = RADIUS) for i in range(NUMBER_OF_PARTICLES)]

particles_list[0].color = "red"

multi_part = MultiParticle(particles_list, SURFACE_WIDTH, SURFACE_HEIGHT)


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
  
# saving to m4 using ffmpeg writer 

# writervideo = FFMpegWriter(fps=FRAMES_NUMBER//VIDEO_DURATION) 
# animation.save(f'{SIMULATION_NAME}.mp4', writer=writervideo) 
# plt.close() 

