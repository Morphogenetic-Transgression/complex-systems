from threading import Thread
import random
import time


import visualization.matplotlib_animation


# class SimulationThread(Thread):
#     def __init__(self, name):
#         Thread.__init__(self)
#         self.name = name

#     def run(self):
#         amount = random.randint(3, 15)
#         time.sleep(amount)

#         # simulation loop


class UIThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        amount = random.randint(3, 9)  # 15
        time.sleep(amount)

        # user interface loop


class VisualizationThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        amount = random.randint(3, 9)  # 15
        time.sleep(amount)

        # visualization loop


if __name__ == "__main__":
    user_interface_thread = UIThread("user_interface")
    user_interface_thread.start()
    visualization_thread = VisualizationThread("visualization")
    visualization_thread.start()
