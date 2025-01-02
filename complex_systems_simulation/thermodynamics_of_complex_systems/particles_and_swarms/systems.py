from typing import List
import numpy as np


class ParticleMechanical():
    
    dimension = 2
    
    def __init__(self, 
                 id,
                 sampling_time: float,
                 mass: float,
                 radius: float,
                 init_state: np.ndarray, 
                 init_velocity: np.ndarray,
                 color="blue"):
        self.id = id
        self.__sampling_time = sampling_time
        self.__mass = mass
        self.__radius = radius
        self.color = color
        self.set_state(init_state)
        self.set_velocity(init_velocity)
     
    @property
    def sampling_time(self):
        return self.__sampling_time
    
    @property
    def mass(self):
        return self.__mass
    
    @property
    def radius(self):
        return self.__radius
    
    @property
    def state(self):
        return self.__state
    
    @property
    def velocity(self):
        return self.__velocity
    
    def set_state(self, state: np.ndarray):
        assert state.shape == (ParticleMechanical.dimension,)
        self.__state = state
        
    def set_velocity(self, velocity: np.ndarray = None):
        if velocity is not None:
            assert velocity.shape == self.state.shape
            self.__velocity = velocity

    def step(self):
        self.set_state(self.state + self.sampling_time * self.velocity)
        

class MultiParticle():
    def __init__(self, 
                 particles: List[ParticleMechanical],
                 width,
                 height,
                 periodic: bool):
        self.__particles = particles
        self.__height, self.__width = height, width
        self.__periodic = periodic

    @property
    def state(self):
        return np.array([particle.state for particle in self.__particles])
    
    def velocities(self):
        return [np.sqrt(np.dot(particle.velocity, 
                               particle.velocity)) for particle in self.__particles]
    
    def colors(self):
        return [particle.color for particle in self.__particles]

    def step(self):
        self.collision_detection()
        for particle in self.__particles:
            particle.step()
            
    def collision_detection(self):
        
        ignore_list = []
        
        for particle in self.__particles:
            if particle in ignore_list:
                continue
            
            x, y = particle.state
            
            if not self.__periodic:
                # with the walls
                
                v_x_next, v_y_next = particle.velocity
                
                if (x > self.__width/2 - particle.radius) or (x < -self.__width/2 + particle.radius):
                    v_x_next = -v_x_next
                if (y > self.__height/2 - particle.radius) or (y < -self.__height/2 + particle.radius):
                    v_y_next = -v_y_next
                    
                v_particle_next = np.array([v_x_next, v_y_next])
                particle.set_velocity(v_particle_next)
                
            else:
                if x > self.__width/2:
                    x = -self.__width/2
                if x < -self.__width/2:
                    x = self.__width/2
                if y > self.__height/2:
                    y = -self.__height/2
                if y < -self.__height/2:
                    y = self.__height/2
                
                
                particle.set_state(np.array([x, y]))
            
            # with neighbour
            for neighbour in self.__particles:
                if id(particle) == id(neighbour):
                    continue
                distance = particle.state - neighbour.state
                if np.dot(distance, distance) <= (particle.radius + neighbour.radius)**2: # collision
                    v1 = particle.velocity
                    v2 = neighbour.velocity
                    m1 = particle.mass
                    m2 = neighbour.mass
                    v_particle_next = v1 - 2*m1/(m1+m2) * np.dot(v1-v2, distance) / np.dot(distance, distance) * distance
                    v_neighbour_next = v2 - 2*m1/(m1+m2) * np.dot(v2-v1, -distance) / np.dot(-distance, -distance) * -distance
                    
                    particle.set_velocity(v_particle_next)
                    neighbour.set_velocity(v_neighbour_next)
                    
                    ignore_list.append(neighbour)
        
        
        '''
        if (abs(-x + (self.__width/2 - particle.radius)) <= self.collision_gap_epsilon or 
            abs(x - (particle.radius - self.__width/2)) <= self.collision_gap_epsilon):
            v_x_next = -v_x_next
        if (abs(-y + (self.__height/2 - particle.radius)) <= self.collision_gap_epsilon or 
            abs(y - (particle.radius - self.__height/2)) <= self.collision_gap_epsilon):
            v_y_next = -v_y_next
        '''
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            