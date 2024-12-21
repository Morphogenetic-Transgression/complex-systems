import numpy as np
import manim as ma


class InformationOfRandomVariableGraph(ma.Scene):
    def construct(self):
        ax = ma.Axes(
            x_range = (0, 1.1, 0.1),
            y_range = (0, 5, 1),
            x_length = 8,
            y_length = 6,
            axis_config={"include_numbers": True},
        ) # on
        y_label = ax.get_y_axis_label(ma.Tex("$-\log_{2}(p(state))$").scale(0.7), 
                                      # edge=ma.LEFT, 
                                      # direction=ma.LEFT,
                                      # buff=0.4
                                     )
        x_label = ax.get_x_axis_label(ma.Tex("$p(state)$").scale(0.7))
        labels = ma.VGroup(x_label, y_label) # on 
        x_range = [0.035, 1]
        graph = ax.plot(lambda x: -np.log2(x), x_range=x_range, use_smoothing=False) # on
        x_dots = np.array([1, 1/2, 1/4, 1/8, 1/16])
        y_dots = -np.log2(x_dots)
        lines = ma.VGroup() # on
        for i in range(1, len(x_dots)):
            xr = x_dots[i-1]
            lines += ax.plot_line_graph(x_values = [x_dots[i], xr],
                                        y_values = [y_dots[i], y_dots[i]],
                                        line_color=ma.GOLD_E,
                                        vertex_dot_style=dict(
                                                              # stroke_width=1,  
                                                              fill_color=ma.GOLD_E
                                                             ),
                                        stroke_width = 4)
        dots = ma.VGroup() # on
        # example_point = ax.c2p(1/6, round(-np.log2(1/6)), 0)
        # dots += ax.get_vertical_line(example_point, color=ma.RED)
        # dots += ma.Dot(example_point, color=ma.RED)
        # dots += ma.Tex("($\\frac{1}{6}$, 3)").scale(0.75).next_to(example_point).shift([-0.3, 0.4, 0]).set_color(ma.RED)
        for i in range(len(x_dots)):
            point = ax.c2p(x_dots[i], y_dots[i], 0)
            if i > 0:
                dots += ax.get_horizontal_line(point, color=ma.BLUE)
                dots += ax.get_vertical_line(point, color=ma.BLUE)
            dots += ma.Dot(point, color=ma.GOLD_E, radius=0.12)
        # title = ma.Title(
        #     # spaces between braces to prevent SyntaxError
        #     r"An Information of a State",
        #     include_underline=False,
        #     font_size=40
        # ) # on
        self.add(ax, 
                 labels, 
                 graph,
                 lines,
                 dots)


class EntropyOfRandomVariableGraph(ma.Scene):
    def construct(self):
        ax = ma.Axes(
            x_range = (0, 1.1, 0.1),
            y_range = (0, 0.6, 0.1),
            x_length = 8,
            y_length = 6,
            axis_config={"include_numbers": True},
        ) # on
        y_label = ax.get_y_axis_label(ma.Tex("$-p(state) \cdot \log_{2}(p(state))$").scale(0.7), 
                                      # edge=ma.LEFT, 
                                      # direction=ma.LEFT,
                                      # buff=0.4
                                     )
        x_label = ax.get_x_axis_label(ma.Tex("$p(state)$").scale(0.7))
        labels = ma.VGroup(x_label, y_label) # on 
        x_range = [0, 1]
        graph = ax.plot(lambda x: 0 if x == 0 else -np.log2(x)*x, x_range=x_range, use_smoothing=False) # on
        
        x_dots = np.array([2**(1/np.log(1/2))])
        y_dots = -x_dots * np.log2(x_dots)
        
        dots = ma.VGroup() # on
        for i in range(len(x_dots)):
            point = ax.c2p(x_dots[i], y_dots[i], 0)
            dots += ax.get_horizontal_line(point, color=ma.BLUE)
            dots += ax.get_vertical_line(point, color=ma.BLUE)
            dots += ma.Dot(point, color=ma.GOLD_E, radius=0.12)  
        dots += (ma.Tex("( $\\frac{1}{2^{\\frac{1}{\ln(2)}}}$, $\\frac{1}{2^{\\frac{1}{\ln(2)}}\ln(2)}$ )")
                 .scale(0.6)
                 .next_to(point)
                 .shift([-0.1, 0.35, 0])
                 .set_color(ma.GOLD_E))
        # title = ma.Title(
        #     # spaces between braces to prevent SyntaxError
        #     r"An Entropy of a State",
        #     include_underline=False,
        #     font_size=40
        # ) # on
        self.add(ax, 
                 labels, 
                 graph,
                 dots)























        