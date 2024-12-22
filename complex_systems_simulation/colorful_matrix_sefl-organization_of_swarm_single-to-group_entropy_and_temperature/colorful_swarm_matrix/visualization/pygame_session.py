# import sys
# import random
import time
import pygame
import pygame_menu
import numpy as np
from ..systems.simulation import Simulation


class PygameShapeDrawer:
    def __init__(self, simulation_area_side_len, cells_number_vertical, cells_number_horizontal, shape_string = "circle"):
        self.cells_number_vertical = cells_number_vertical
        self.cells_number_horizontal = cells_number_horizontal
        self.shape_string = shape_string
        if self.cells_number_vertical != self.cells_number_horizontal:
            self.shape_string = "rectangle"
        self.w = simulation_area_side_len / self.cells_number_horizontal
        self.h = simulation_area_side_len / self.cells_number_vertical
        self.diameter = min(self.w, self.h) # cell area side size / square area side size
        self.radius = self.diameter / 2

    def draw_circle(self, screen, color, x, y):
        return pygame.draw.circle(screen,
                                  color,
                                  [x, y],
                                  self.radius,
                                  0)

    def draw_rectangle(self, screen, color, x, y):
        return pygame.draw.rect(screen, 
                                color, 
                                pygame.Rect(x, y, self.w, self.h))

    def draw_shape(self, screen, color, x, y):
        if self.shape_string == "circle":
            return self.draw_circle(screen, color, x, y)
        elif self.shape_string == "rectangle":
            return self.draw_rectangle(screen, color, x, y)
        else:
            assert False, "not existing shape"
            

class PygameSession:
    def __init__(self, simulation: Simulation, by_mouse: bool, rendering_duration: float = 0.1):
        # simulation
        self.simulation = simulation 
        self.__simulation_steps = self.simulation.steps_number
        self.rows_number, self.columns_number, _ = self.simulation.group.state.shape
        # pygame
        self.by_mouse = by_mouse
        self.visualization_title = 'TODO simulation title'
        self.rendering_duration = rendering_duration
        self.screen_size = [1100, 900]
        self.meridian = self.screen_size[0] / 2 - 0.1 * self.screen_size[0]
        self.equator = self.screen_size[1] / 2
        self.white = 250
        # self.screen_color = [self.white, self.white, self.white]
        self.screen_color = [self.white, self.white, self.white]
        # self.cell_color = pygame.Color("aquamarine")
        # self.simulation_area_side_len = 800 
        # self.simulation_area_side_len = 600 
        self.simulation_area_side_len = 400
        self.cells_drawer = PygameShapeDrawer(simulation_area_side_len = self.simulation_area_side_len, 
                                              cells_number_vertical = self.rows_number, 
                                              cells_number_horizontal = self.columns_number,
                                              shape_string = "circle")
        # writings
        self.font_size = 20
        

    def simulation_steps(self):
        return self.__simulation_steps

    def metrics_strings(self):
        return [f"Simulation Steps Left: {self.simulation_steps()}",
                f"Number of Columns: {self.columns_number}",
                f"Number of Rows: {self.rows_number}",
                f"''Температура'': -{self.simulation.group.temperature()}",
                f"''Однородность'': {self.simulation.group.temperature()}"]
        
    def draw_text(self, text: str, x, y):
        green = (0, 255, 0)
        blue = (0, 0, 128)
        # create a text surface object,
        # on which text is drawn on it.
        text = self.font.render(text, True, green, blue)
        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()
        # set the center of the rectangular object.
        textRect.center = (x, y)
        # copying the text surface object
        # to the display surface object
        # at the center coordinate.
        self.screen.blit(text, textRect)
        
    def draw_metrics_table(self):
        # TODO make understendable
        table_coords = [0.85 * self.screen_size[0], 0.03 * self.screen_size[1]]
        self.font = pygame.font.Font('freesansbold.ttf', self.font_size)
        metrics_strings = self.metrics_strings()
        for m in range(len(metrics_strings)):
            metric_string = metrics_strings[m]
            text_x = table_coords[0]
            text_y = table_coords[1] + m * self.font_size
            if m == 3:
                text_y += 100
            elif m == 4:
                text_y += 200
            self.draw_text(metric_string, text_x, text_y)

    def decrement_group_temperature(self):
        current = self.simulation.group.temperature()
        next = current - 1
        self.simulation.group.set_temperature(next)
        self.simulation.group.set_communication()

    def increment_group_temperature(self):
        current = self.simulation.group.temperature()
        next = current + 1
        self.simulation.group.set_temperature(next)
        self.simulation.group.set_communication()

    # def np_to_rgb250(self, rgb_normalized_np) -> Tuple[int]:
    #     return tuple(np.round(rgb_normalized_np*self.white).astype(int))

    def draw_cell(self, cell_color, x, y):
        return self.cells_drawer.draw_shape(self.screen,
                                            cell_color,
                                            x,
                                            y)
        
    def draw_column(self, column, x, y):
        for i in range(self.rows_number):
            cell_rgb_normalized = column[i]
            # cell_color = self.np_to_rgb250(cell_rgb_normalized)
            
            cell_color = tuple(np.round(50+cell_rgb_normalized*100).astype(int))
            
            cell = self.draw_cell(cell_color, x, y + i * self.cells_drawer.h) 
    
    def draw_matrix(self, matrix: np.ndarray):
        x_for_all = self.meridian - self.cells_drawer.w * (self.columns_number + 4) / 2 # + 4
        y_for_all = self.equator - self.cells_drawer.h * (self.rows_number - 4) / 2 # -6
        for j in range(self.columns_number):
            self.draw_column(matrix[: , j], x_for_all + (j) * self.cells_drawer.w, y_for_all)
            # self.draw_column(matrix[: , j].reshape((self.rows_number, 1)), x_for_all + (j) * self.cells_drawer.w, y_for_all)

    def draw_snap(self, group_state: np.ndarray):
        self.draw_matrix(group_state)
        pygame.display.flip()
        self.__simulation_steps -= 1
        self.continue_simulation = False
        
    def draw_simulation(self):
        # init simulation screen
        pygame.init()
        pygame.display.set_caption(self.visualization_title)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen.fill(self.screen_color)
        # draw init state
        self.draw_snap(self.simulation.group.state)
        # running rutin
        self.running = True
        
        while self.running:
            
            time.sleep(self.rendering_duration)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.continue_simulation = True
                    
            if not self.by_mouse:
                self.continue_simulation = True

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_LEFT]:
                self.decrement_group_temperature()
            if pressed_keys[pygame.K_RIGHT]:
                self.increment_group_temperature()

            self.draw_metrics_table()
            
            if self.continue_simulation and self.__simulation_steps > 0:
                self.draw_snap(next(self.simulation))
        
        pygame.quit()        
        

    


