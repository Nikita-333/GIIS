import math
import tkinter as tk
from LineDraw import LineAlgorithms
from Curve import CurveAlgorithms
from ParamCurve import ParamCurveAlgorithms


# https://www.rosettacode.org/wiki/Xiaolin_Wu%27s_line_algorithm
# https://grafika.me/node/36

class LineDrawerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Line Drawer")
        self.master.geometry("1210x660")

        self.canvas = tk.Canvas(master, width=1000, height=600)
        self.canvas.pack()

        self.line_algorithms = LineAlgorithms(self.canvas)
        self.curve_algorithms = CurveAlgorithms(self.canvas)
        self.param_algorithms = ParamCurveAlgorithms(self.canvas)

        self.create_menu()
        self.selected_algorithm = None


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

        parabola_button = tk.Button(self.menu_frame, text="Эрмит", command=self.select_hermit_algorithm)
        parabola_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="nw")

        bezier_button = tk.Button(self.menu_frame, text="Безье", command=self.select_bezier_curve)
        bezier_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="nw")

        bspline_button = tk.Button(self.menu_frame, text="В-Сплайн", command=self.select_bspline)
        bspline_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="nw")

        clear_button = tk.Button(self.menu_frame, text="Очистка", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="nw")

        debug_button = tk.Button(self.menu_frame, text="Откладка", command=self.show_actions)
        debug_button.pack(side=tk.LEFT, padx=5, pady=5, anchor="nw")

    def select_dda_algorithm(self):
        self.selected_algorithm = self.line_algorithms.draw_dda_algorithm

    def select_bresenham_algorithm(self):
        self.selected_algorithm = self.line_algorithms.draw_line_bresenham

    def select_wu_algorithm(self):
        self.selected_algorithm = self.line_algorithms.draw_line_wu

    def select_circle_bresenham_algorithm(self):
        self.selected_algorithm = self.curve_algorithms.draw_circle_bresenham

    def select_ellipse_bresenham_algorithm(self):
        self.selected_algorithm = self.curve_algorithms.draw_ellipse_bresenham

    def select_hyperbola_bresenham_algorithm(self):
        self.selected_algorithm = self.curve_algorithms.draw_hyperbola_bresenham

    def select_parabola_bresenham_algorithm(self):
        self.selected_algorithm = self.curve_algorithms.draw_parabola_bresenham

    def select_hermit_algorithm(self):
        self.selected_algorithm = self.param_algorithms.draw_hermit

    def select_bezier_curve(self):
        self.selected_algorithm = self.param_algorithms.draw_bezier_curve

    def select_bspline(self):
        self.selected_algorithm = self.param_algorithms.draw_b_spline

    def clear_canvas(self):
        self.canvas.delete("all")

    def show_actions(self):
        debug_window = tk.Toplevel(self.master)
        debug_window.title("Отладка")
        debug_window.geometry("400x300")

        action_listbox = tk.Listbox(debug_window)
        action_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for action in self.line_algorithms.action_list:
            action_listbox.insert(tk.END, action)

        for action in self.curve_algorithms.action_list:
            action_listbox.insert(tk.END, action)

        for action in self.param_algorithms.action_list:
            action_listbox.insert(tk.END,action)

        debug_window.mainloop()

    def on_canvas_click(self, event):
        if self.selected_algorithm:
            self.selected_algorithm(event)

    def run(self):
        self.master.resizable(width=False, height=False)
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LineDrawerApp(root)
    app.canvas.bind("<Button-1>", app.on_canvas_click)
    app.canvas.bind("<Button-3>", app.param_algorithms.right_click_point)
    app.canvas.bind("<Button-1>", app.param_algorithms.left_click_draw)
    app.run()