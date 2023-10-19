import math


class CurveAlgorithms:
    def __init__(self, canvas):
        self.selected_algorithm = None
        self.canvas = canvas
        self.start_point = None
        self.action_list = []

    def add_action(self, action):
        self.action_list.append(action)

    def draw_circle_bresenham_algo(self, center, radius):
        x_center, y_center = center
        x = 0
        y = radius
        d = 3 - 2 * radius
        self.draw_symmetric_points(x, y, x_center, y_center, figure='Circle')
        while x <= y:
            #внутри окружности
            if d < 0:
                d += 4 * x + 6
            else:
                # на границе
                d += 4 * (x - y) + 10
                y -= 1
            x += 1
            self.draw_symmetric_points(x, y, x_center, y_center, figure='Circle')

    def draw_ellipse_bresenham_algo(self, center, radius_x, radius_y):
        x_center, y_center = center
        x = 0
        y = radius_y
        # начальное значение дискриминанта для первой половины эллипса
        d1 = (radius_y * radius_y) - (radius_x * radius_x * radius_y) + (0.25 * radius_x * radius_x)
        dx = 2 * radius_y * radius_y * x
        dy = 2 * radius_x * radius_x * y

        #для верхней половины эллипса
        while dx < dy:
            self.draw_symmetric_points(x, y, x_center, y_center, figure='Ellipse')
            #Дискриминат для верхней половины
            if d1 < 0:
                x += 1
                dx += 2 * radius_y * radius_y
                d1 += dx + radius_y * radius_y
            else:
                x += 1
                y -= 1
                dx += 2 * radius_y * radius_y
                dy -= 2 * radius_x * radius_x
                d1 += dx - dy + radius_y * radius_y

        d2 = (radius_y * radius_y) * (x + 0.5) * (x + 0.5) + (radius_x * radius_x) * (y - 1) * (y - 1) - (
                radius_x * radius_x * radius_y * radius_y)
        #нижней половины эллипса
        while y >= 0:
            self.draw_symmetric_points(x, y, x_center, y_center, figure='Ellipse')
        #Дискриминат для нижней половины
            if d2 > 0:
                y -= 1
                dy -= 2 * radius_x * radius_x
                d2 += radius_x * radius_x - dy
            else:
                y -= 1
                x += 1
                dx += 2 * radius_y * radius_y
                dy -= 2 * radius_x * radius_x
                d2 += dx - dy + radius_x * radius_x

    def draw_symmetric_points(self, x, y, x_center, y_center, figure=None):
        if figure == 'Ellipse':
            self.canvas.create_rectangle(x_center + x, y_center + y, x_center + x + 1, y_center + y + 1, fill="blue")
            self.canvas.create_rectangle(x_center - x, y_center + y, x_center - x + 1, y_center + y + 1, fill="blue")
            self.canvas.create_rectangle(x_center + x, y_center - y, x_center + x + 1, y_center - y + 1, fill="blue")
            self.canvas.create_rectangle(x_center - x, y_center - y, x_center - x + 1, y_center - y + 1, fill="blue")

        if figure == 'Circle':
            self.canvas.create_rectangle(x_center + x, y_center + y, x_center + x + 1, y_center + y + 1, fill="blue")
            self.canvas.create_rectangle(x_center - x, y_center + y, x_center - x + 1, y_center + y + 1, fill="blue")
            self.canvas.create_rectangle(x_center + x, y_center - y, x_center + x + 1, y_center - y + 1, fill="blue")
            self.canvas.create_rectangle(x_center - x, y_center - y, x_center - x + 1, y_center - y + 1, fill="blue")
            self.canvas.create_rectangle(x_center + y, y_center + x, x_center + y + 1, y_center + x + 1, fill="blue")
            self.canvas.create_rectangle(x_center - y, y_center + x, x_center - y + 1, y_center + x + 1, fill="blue")
            self.canvas.create_rectangle(x_center + y, y_center - x, x_center + y + 1, y_center - x + 1, fill="blue")
            self.canvas.create_rectangle(x_center - y, y_center - x, x_center - y + 1, y_center - x + 1, fill="blue")

    def draw_parabola_bresenham_algo(self, start_point, end_point):
        h, k = start_point
        delta_x = end_point[0] - start_point[0]
        delta_y = end_point[1] - start_point[1]
        t_min = -max(abs(delta_x), abs(delta_y)) / 2
        t_max = max(abs(delta_x), abs(delta_y)) / 2

        dt = 0.01

        t = t_min
        while t <= t_max:
            x = h + t
            if delta_y > 0:
                y = k + t ** 2
            else:
                y = k - t ** 2
            self.canvas.create_oval(x, y, x, y, width=1)
            t += dt

    def draw_hyperbola_bresenham_algo(self, center, a, b):
        h, k = center
        t_min = -1.0
        t_max = 1.0
        dt = 0.1

        prev_x, prev_y = None, None

        t = t_min
        while t < t_max:
            x1 = h + a * math.cosh(t)
            y1 = k + b * math.sinh(t)

            if prev_x is not None and prev_y is not None:
                self.canvas.create_line(prev_x, prev_y, x1, y1, width=1)
                self.canvas.create_line(2 * h - prev_x, prev_y, 2 * h - x1, y1)
            prev_x, prev_y = x1, y1
            t += dt

    def draw_circle_bresenham(self, event):
        if self.start_point is None:
            self.start_point = (event.x, event.y)
            self.add_action("Брезенхем для окружности: Начальная точка: ({}, {})".format(event.x, event.y))
            return

        end_point = (event.x, event.y)
        radius = int(math.hypot(end_point[0] - self.start_point[0], end_point[1] - self.start_point[1]))
        center = self.start_point
        self.add_action(
            "Брезенхем для окружности: Конечная точка: ({}, {}), Радиус: {}".format(event.x, event.y, radius))
        self.draw_circle_bresenham_algo(center, radius)
        self.start_point = None

    def draw_ellipse_bresenham(self, event):
        if self.start_point is None:
            self.start_point = (event.x, event.y)
            self.add_action("Брезенхем для эллипса: Начальная точка: ({}, {})".format(event.x, event.y))
            return

        end_point = (event.x, event.y)
        radius_x = abs(end_point[0] - self.start_point[0])
        radius_y = abs(end_point[1] - self.start_point[1])
        center = self.start_point
        self.add_action(
            "Брезенхем для эллипса: Конечная точка: ({}, {}), Большой радиус: {}, Малый радиус: {}".format(
                event.x, event.y, radius_x, radius_y))
        self.draw_ellipse_bresenham_algo(center, radius_x, radius_y)
        self.start_point = None

    def draw_hyperbola_bresenham(self, event):
        if self.start_point is None:
            self.start_point = (event.x, event.y)
            self.add_action("Гипербола: Начальная точка: ({}, {})".format(event.x, event.y))
            return

        end_point = (event.x, event.y)
        a = abs(end_point[0] - self.start_point[0])
        b = abs(end_point[1] - self.start_point[1])
        center = self.start_point
        self.add_action("Гипербола: Конечная точка: ({}, {}), Радиусы (a, b): ({}, {})".format(event.x, event.y, a, b))
        self.draw_hyperbola_bresenham_algo(center, a, b)
        self.start_point = None

    def draw_parabola_bresenham(self, event):
        if self.start_point is None:
            self.start_point = (event.x, event.y)
            self.add_action("Брезенхем для параболы: Начальная точка: ({}, {})".format(event.x, event.y))
            return

        end_point = (event.x, event.y)
        self.add_action("Брезенхем для параболы: Конечная точка: ({}, {})".format(event.x, event.y))
        self.draw_parabola_bresenham_algo(self.start_point, end_point)
        self.start_point = None

    def select_circle_bresenham_algorithm(self):
        self.selected_algorithm = self.draw_circle_bresenham

    def select_ellipse_bresenham_algorithm(self):
        self.selected_algorithm = self.draw_ellipse_bresenham

    def select_hyperbola_bresenham_algorithm(self):
        self.selected_algorithm = self.draw_hyperbola_bresenham

    def select_parabola_bresenham_algorithm(self):
        self.selected_algorithm = self.draw_parabola_bresenham