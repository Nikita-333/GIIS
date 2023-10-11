import math
import tkinter as tk


# https://www.rosettacode.org/wiki/Xiaolin_Wu%27s_line_algorithm
# https://grafika.me/node/36

class LineDrawerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Line Drawer")
        self.master.geometry("950x660")

        self.canvas = tk.Canvas(master, width=950, height=600)
        self.canvas.pack()

        self.create_menu()
        self.selected_algorithm = None
        self.start_point = None
        self.action_list = []

    def create_menu(self):
        self.menu_frame = tk.Frame(self.master)
        self.menu_frame.pack(pady=10, padx=10, fill=tk.X)

        dda_button = tk.Button(self.menu_frame, text="ЦДА", command=self.select_dda_algorithm)
        dda_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="nw")

        bresenham_button = tk.Button(self.menu_frame, text="Брезенхем", command=self.select_bresenham_algorithm)
        bresenham_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="nw")

        wu_button = tk.Button(self.menu_frame, text="Алгоритм Ву", command=self.select_wu_algorithm)
        wu_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="nw")

        circle_button = tk.Button(self.menu_frame, text="Окружность", command=self.select_circle_bresenham_algorithm)
        circle_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="nw")

        ellipse_button = tk.Button(self.menu_frame, text="Эллипс", command=self.select_ellipse_bresenham_algorithm)
        ellipse_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="nw")

        hyperbola_button = tk.Button(self.menu_frame, text="Гипербола",
                                     command=self.select_hyperbola_bresenham_algorithm)
        hyperbola_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="nw")

        parabola_button = tk.Button(self.menu_frame, text="Парабола", command=self.select_parabola_bresenham_algorithm)
        parabola_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="nw")

        clear_button = tk.Button(self.menu_frame, text="Очистка", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="nw")

        debug_button = tk.Button(self.menu_frame, text="Откладка", command=self.show_actions)
        debug_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="nw")

    def clear_canvas(self):
        self.canvas.delete("all")

    def select_circle_bresenham_algorithm(self):
        self.selected_algorithm = self.draw_circle_bresenham

    def select_ellipse_bresenham_algorithm(self):
        self.selected_algorithm = self.draw_ellipse_bresenham

    def select_hyperbola_bresenham_algorithm(self):
        self.selected_algorithm = self.draw_hyperbola_bresenham

    def select_parabola_bresenham_algorithm(self):
        self.selected_algorithm = self.draw_parabola_bresenham

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

    def draw_circle_bresenham_algo(self, center, radius):
        x_center, y_center = center
        x = 0
        y = radius
        d = 3 - 2 * radius
        self.draw_symmetric_points(x, y, x_center, y_center, figure='Circle')
        while x <= y:
            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1
            self.draw_symmetric_points(x, y, x_center, y_center, figure='Circle')

    def draw_ellipse_bresenham_algo(self, center, radius_x, radius_y):
        x_center, y_center = center
        x = 0
        y = radius_y
        d1 = (radius_y * radius_y) - (radius_x * radius_x * radius_y) + (0.25 * radius_x * radius_x)
        dx = 2 * radius_y * radius_y * x
        dy = 2 * radius_x * radius_x * y

        while dx < dy:
            self.draw_symmetric_points(x, y, x_center, y_center, figure='Ellipse')
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

        while y >= 0:
            self.draw_symmetric_points(x, y, x_center, y_center, figure='Ellipse')
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
    def select_dda_algorithm(self):
        self.selected_algorithm = self.draw_line_dda

    def select_bresenham_algorithm(self):
        self.selected_algorithm = self.draw_line_bresenham

    def select_wu_algorithm(self):
        self.selected_algorithm = self.draw_line_wu

    def draw_line_dda(self, event):
        if self.start_point is None:
            self.start_point = (event.x, event.y)
            self.add_action("ЦДА: Начальная точка: ({}, {})".format(event.x, event.y))
            return

        end_point = (event.x, event.y)
        self.add_action("ЦДА: Конечная точка: ({}, {})".format(event.x, event.y))
        self.draw_line(self.start_point, end_point)
        self.start_point = None

    def draw_line_bresenham(self, event):
        if self.start_point is None:
            self.start_point = (event.x, event.y)
            self.add_action("Брезенхем: Начальная точка: ({}, {})".format(event.x, event.y))
            return

        end_point = (event.x, event.y)
        self.add_action("Брезенхем: Конечная точка: ({}, {})".format(event.x, event.y))
        self.draw_line_bresenham_algo(self.start_point, end_point)
        self.start_point = None

    def draw_line_wu(self, event):
        if self.start_point is None:
            self.start_point = (event.x, event.y)
            self.add_action("Алгоритм Ву: Начальная точка: ({}, {})".format(event.x, event.y))
            return

        end_point = (event.x, event.y)
        self.add_action("Алгоритм Ву: Конечная точка: ({}, {})".format(event.x, event.y))
        self.draw_line_wu_algo(self.start_point, end_point)
        self.start_point = None

    def add_action(self, action):
        self.action_list.append(action)

    def show_actions(self):
        debug_window = tk.Toplevel(self.master)
        debug_window.title("Отладка")
        debug_window.geometry("380x300")

        action_listbox = tk.Listbox(debug_window)
        action_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for action in self.action_list:
            action_listbox.insert(tk.END, action)

        debug_window.mainloop()

    def draw_line(self, start_point, end_point):
        x1, y1 = start_point
        x2, y2 = end_point

        dx = x2 - x1
        dy = y2 - y1

        steps = max(abs(dx), abs(dy))
        x_increment = dx / steps
        y_increment = dy / steps

        x, y = x1, y1
        for _ in range(int(steps) + 1):
            self.canvas.create_rectangle(x, y, x + 1, y + 1, fill="black")
            x += x_increment
            y += y_increment

    def draw_line_bresenham_algo(self, start_point, end_point):
        x1, y1 = start_point
        x2, y2 = end_point

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        x, y = x1, y1
        while True:
            self.canvas.create_rectangle(x, y, x + 1, y + 1, fill="blue")
            if x == x2 and y == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def draw_line_wu_algo(self, start_point, end_point):
        x1, y1 = start_point
        x2, y2 = end_point

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        steep = dy > dx

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = x2 - x1
        dy = y2 - y1
        gradient = float(dy) / float(dx) if dx != 0 else 1.0

        xend = round(x1)
        yend = y1 + gradient * (xend - x1)
        xgap = 1 - fractional_part(x1 + 0.5)
        xpxl1 = xend
        ypxl1 = int(yend)

        if steep:
            self.draw_pixel(ypxl1, xpxl1, xgap, 1)
        else:
            self.draw_pixel(xpxl1, ypxl1, xgap, 1)

        intery = yend + gradient

        xend = round(x2)
        yend = y2 + gradient * (xend - x2)
        xgap = fractional_part(x2 + 0.5)
        xpxl2 = xend
        ypxl2 = int(yend)

        if steep:
            self.draw_pixel(ypxl2, xpxl2, 1 - xgap, 1)
        else:
            self.draw_pixel(xpxl2, ypxl2, 1 - xgap, 1)

        if steep:
            for x in range(int(xpxl1 + 1), int(xpxl2)):
                self.draw_pixel(int(intery), x, 1 - fractional_part(intery), fractional_part(intery))
                self.draw_pixel(int(intery) + 1, x, fractional_part(intery), 1 - fractional_part(intery))
                intery += gradient
        else:
            for x in range(int(xpxl1 + 1), int(xpxl2)):
                self.draw_pixel(x, int(intery), 1 - fractional_part(intery), fractional_part(intery))
                self.draw_pixel(x, int(intery) + 1, fractional_part(intery), 1 - fractional_part(intery))
                intery += gradient

    def draw_pixel(self, x, y, c1, c2):
        color1 = int(c1 * 255)
        color2 = int(c2 * 255)
        self.canvas.create_rectangle(x, y, x + 1, y + 1, fill=f"#{color1:02x}{color1:02x}{color1:02x}")
        self.canvas.create_rectangle(x, y + 1, x + 1, y + 1, fill=f"#{color2:02x}{color2:02x}{color2:02x}")

    def on_canvas_click(self, event):
        if self.selected_algorithm:
            self.selected_algorithm(event)

    def run(self):
        self.master.resizable(width=False, height=False)
        self.master.mainloop()

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

def fractional_part(x):
    return x - int(x)


if __name__ == "__main__":
    root = tk.Tk()
    app = LineDrawerApp(root)
    app.canvas.bind("<Button-1>", app.on_canvas_click)
    app.run()
