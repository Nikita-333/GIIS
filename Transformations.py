import tkinter as tk

class CubeDrawer:
    def __init__(self, canvas):
        self.action_list = []
        self.start_point = None
        self.selected_algorithm = None

        self.canvas = canvas
        self.canvas.pack()

        self.cube_size = 100

    def draw_cube(self,start_point, end_point):

        if start_point is None or end_point is None:
            return

        # Координаты куба
        x0, y0 = start_point
        x1, y1 = end_point[0], start_point[1]
        x2, y2 = end_point
        x3, y3 = start_point[0], end_point[1]

        # Рисуем переднюю грань
        self.canvas.create_line(x0, y0, x1, y1)
        self.canvas.create_line(x1, y1, x2, y2)
        self.canvas.create_line(x2, y2, x3, y3)
        self.canvas.create_line(x3, y3, x0, y0)

        # Рисуем заднюю грань
        x4, y4 = x0 + self.cube_size / 4, y0 - self.cube_size / 4
        x5, y5 = x1 + self.cube_size / 4, y1 - self.cube_size / 4
        x6, y6 = x2 + self.cube_size / 4, y2 - self.cube_size / 4
        x7, y7 = x3 + self.cube_size / 4, y3 - self.cube_size / 4

        self.canvas.create_line(x4, y4, x5, y5)
        self.canvas.create_line(x5, y5, x6, y6)
        self.canvas.create_line(x6, y6, x7, y7)
        self.canvas.create_line(x7, y7, x4, y4)

        self.canvas.create_line(x0, y0, x4, y4)
        self.canvas.create_line(x1, y1, x5, y5)
        self.canvas.create_line(x2, y2, x6, y6)
        self.canvas.create_line(x3, y3, x7, y7)

    def draw_cube_algorithms(self, event):
        if self.start_point is None:
            self.start_point = (event.x, event.y)
            #self.add_action("Куб: Начальная точка: ({}, {})".format(event.x, event.y))
            return

        end_point = (event.x, event.y)
        #self.add_action("Куб: Конечная точка: ({}, {})".format(event.x, event.y))
        self.draw_cube(self.start_point, end_point)
        self.start_point = None

    def select_cube_algorithm(self):
        self.selected_algorithm = self.draw_cube_algorithms

    def add_action(self, action):
        self.action_list.append(action)

