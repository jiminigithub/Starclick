import tkinter as tk
import math

CANVAS_WIDTH = 600  # Aumentado para acomodar a nova estrela
CANVAS_HEIGHT = 400
CENTER_X = CANVAS_WIDTH / 3  # Ajustado para centralizar a estrela original
CENTER_Y = CANVAS_HEIGHT / 2
RADIUS_OUTER = 150
RADIUS_INNER = 60
POINT_RADIUS = 10
NEW_STAR_OFFSET_X = 400  # Deslocamento X para a nova estrela
NEW_STAR_OFFSET_Y = 200  # Deslocamento Y para a nova estrela
NEW_STAR_SCALE = 0.5   # Escala para o tamanho da nova estrela

class StarApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.pack()
        self.reset_button = tk.Button(root, text="Resetar Estrelas", command=self.reset_stars)
        self.reset_button.pack()
        self.initialize_stars()

    def initialize_stars(self):
        self.canvas.delete("all")  # Limpa o canvas
        self.points = self.calculate_star_points(CENTER_X, CENTER_Y, RADIUS_OUTER, RADIUS_INNER)
        self.new_star_points = []
        self.clicked_points = [False] * 10
        self.new_star_clicked_points = []
        self.draw_star()
        self.canvas.bind("<Button-1>", self.on_click)  # Re-vincula o evento de clique

    def calculate_star_points(self, cx, cy, r_outer, r_inner):
        points = []
        angle = math.pi / 2  # Ângulo inicial apontando para cima

        # Alternar entre pontos externos e internos
        for i in range(10):
            r = r_inner if i % 2 else r_outer
            x = cx + r * math.cos(angle)
            y = cy - r * math.sin(angle)
            points.append((x, y))
            angle += math.pi / 5  # Mover para o próximo ponto (36 graus)

        return points

    def draw_star(self):
        self.canvas.create_polygon(self.points, fill='yellow', outline='black')
        for px, py in self.points:
            self.canvas.create_oval(px - POINT_RADIUS, py - POINT_RADIUS, px + POINT_RADIUS, py + POINT_RADIUS, fill='red')

    def on_click(self, event):
        x, y = event.x, event.y
        # Verifica cliques na estrela original
        for i, (px, py) in enumerate(self.points):
            if self.is_within_click_range(x, y, px, py):
                if not self.clicked_points[i]:
                    self.handle_point_click(i, px, py)
                return  # Finaliza o método se um ponto foi clicado

        # Verifica cliques na nova estrela
        for i, (px, py) in enumerate(self.new_star_points):
            if self.is_within_click_range(x, y, px, py):
                if not self.new_star_clicked_points[i]:
                    self.handle_point_click(i, px, py, new_star=True)
                return  # Finaliza o método se um ponto foi clicado

    def handle_point_click(self, i, px, py, new_star=False):
        value = 2 ** (i + 1)
        print(f"Point {i + 1} value: {value}")
        self.canvas.create_text(px, py, text=str(value), fill='blue')
        if new_star:
            self.new_star_clicked_points[i] = True
        else:
            self.clicked_points[i] = True
            if all(self.clicked_points):
                self.draw_new_star()

    def is_within_click_range(self, x, y, px, py, radius=POINT_RADIUS):
        return (x - px) ** 2 + (y - py) ** 2 <= radius ** 2

    def draw_new_star(self):
        # Calcula os pontos para a nova estrela
        new_center_x = NEW_STAR_OFFSET_X
        new_center_y = NEW_STAR_OFFSET_Y
        new_radius_outer = RADIUS_OUTER * NEW_STAR_SCALE
        new_radius_inner = RADIUS_INNER * NEW_STAR_SCALE
        self.new_star_points = self.calculate_star_points(new_center_x, new_center_y, new_radius_outer,
                                                          new_radius_inner)
        self.new_star_clicked_points = [False] * len(self.new_star_points)  # Inicializa a lista de cliques

        # Desenha a nova estrela
        self.canvas.create_polygon(self.new_star_points, fill='yellow', outline='black')
        for px, py in self.new_star_points:
            self.canvas.create_oval(px - POINT_RADIUS, py - POINT_RADIUS, px + POINT_RADIUS, py + POINT_RADIUS,
                                    fill='red')

    def reset_stars(self):
        self.canvas.delete("all")  # Limpa o canvas
        self.initialize_stars()  # Reinicia o estado das estrelas

if __name__ == '__main__':
    root = tk.Tk()
    root.title("StarExp - Exponential Star")
    app = StarApp(root)
    root.mainloop()
