import numpy as np
from scipy import interpolate

class ParamCurveAlgorithms:

    def __init__(self, canvas):
        self.selected_algorithm = None
        self.canvas = canvas
        self.start_point = None
        self.action_list = []
        self.start_point = None
        self.end_point = None

    def add_action(self, action):
        self.action_list.append(action)

    def draw_hermit(self, event):
        if self.start_point is None:
            self.start_point = (event.x, event.y)
            self.add_action("Форма для Хермит: Начальная точка: ({}, {})".format(event.x, event.y))
            return

        end_point = (event.x, event.y)
        self.add_action("Форма для Хермит: Конечная точка: ({}, {})".format(event.x, event.y))
        self.draw_hermit_algo(self.start_point, end_point)
        self.start_point = None

    def draw_hermit_algo(self, start_point, end_point):

        x0, y0 = start_point
        x1, y1 = end_point

        tangent_start = (200, 0)
        tangent_end = (0, -200)

        for t in range(0, 101):
            t /= 100.0
            t2 = t * t
            t3 = t2 * t
            x = (2 * t3 - 3 * t2 + 1) * x0 + (t3 - 2 * t2 + t) * tangent_start[0] + (-2 * t3 + 3 * t2) * x1 + (
                        t3 - t2) * tangent_end[0]
            y = (2 * t3 - 3 * t2 + 1) * y0 + (t3 - 2 * t2 + t) * tangent_start[1] + (-2 * t3 + 3 * t2) * y1 + (
                        t3 - t2) * tangent_end[1]
            self.canvas.create_rectangle(x, y, x + 1, y + 1)

    def draw_bezier_curve(self, event):
        if self.start_point is None:
            self.start_point = (event.x, event.y)
            self.add_action("Форма для Безье: Начальная точка: ({}, {})".format(event.x, event.y))
            return

        if self.end_point is None:
            self.end_point = (event.x, event.y)
            self.add_action("Форма для Безье: Конечная точка: ({}, {})".format(event.x, event.y))
            return

        # Создаем две дополнительные точки
        control_point1 = (event.x, self.start_point[1])
        control_point2 = (self.end_point[0], event.y)

        # Формируем список из четырех контрольных точек
        control_points = [self.start_point, control_point1, control_point2, self.end_point]
        self.draw_bezier_curve_algo(control_points)
        self.start_point = None
        self.end_point = None

    def draw_bezier_curve_algo(self, control_points):
        if len(control_points) != 4:
            print("Для кривой Безье требуется 4 контрольные точки.")
            return

        P0, P1, P2, P3 = control_points

        steps = 100
        delta_t = 1.0 / steps

        x_coords = []
        y_coords = []

        for i in range(steps + 1):
            t = i * delta_t
            u = 1 - t
            x = u ** 3 * P0[0] + 3 * u ** 2 * t * P1[0] + 3 * u * t ** 2 * P2[0] + t ** 3 * P3[0]
            y = u ** 3 * P0[1] + 3 * u ** 2 * t * P1[1] + 3 * u * t ** 2 * P2[1] + t ** 3 * P3[1]

            x_coords.append(x)
            y_coords.append(y)

        for i in range(steps):
            x1, y1 = x_coords[i], y_coords[i]
            x2, y2 = x_coords[i + 1], y_coords[i + 1]
            self.canvas.create_line(x1, y1, x2, y2)

    def select_bezier_curve(self):
        self.selected_algorithm = self.draw_bezier_curve

    def select_hermit_algorithm(self):
        self.selected_algorithm = self.draw_hermit
