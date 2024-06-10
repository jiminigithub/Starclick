import tkinter as tk
from PIL import Image, ImageTk
import math
import os

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400
CENTER_X = CANVAS_WIDTH / 3
CENTER_Y = CANVAS_HEIGHT / 2
RADIUS_OUTER = 150
RADIUS_INNER = 60
POINT_RADIUS = 10
NEW_STAR_OFFSET_X = 400
NEW_STAR_OFFSET_Y = 200
NEW_STAR_SCALE = 0.5

# Ajuste o caminho para a imagem da estrela e do fundo
STAR_IMAGE_PATH = "Starclick/img/star.png"
BACKGROUND_IMAGE_PATH = "Starclick/img//4k-ultra-hd-galaxy.jpg"

class StarApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.pack()

        # Verificar se os caminhos das imagens são válidos
        if not os.path.exists(STAR_IMAGE_PATH):
            print(f"Erro: O caminho da imagem da estrela {STAR_IMAGE_PATH} não é válido.")
            return
        if not os.path.exists(BACKGROUND_IMAGE_PATH):
            print(f"Erro: O caminho da imagem de fundo {BACKGROUND_IMAGE_PATH} não é válido.")
            return

        # Carregar a imagem de fundo
        self.bg_image = Image.open(BACKGROUND_IMAGE_PATH)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor=tk.NW)

        self.reset_button = tk.Button(root, text="Resetar Estrelas", command=self.reset_stars)
        self.reset_button.pack()
        self.initialize_stars()

    def initialize_stars(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor=tk.NW)  # Re-desenha a imagem de fundo
        self.points = self.calculate_star_points(CENTER_X, CENTER_Y, RADIUS_OUTER, RADIUS_INNER)
        self.new_star_points = []
        self.clicked_points = [False] * 10
        self.new_star_clicked_points = []
        self.draw_star()
        self.canvas.bind("<Button-1>", self.on_click)

    def calculate_star_points(self, cx, cy, r_outer, r_inner):
        points = []
        angle = math.pi / 2

        for i in range(10):
            r = r_inner if i % 2 else r_outer
            x = cx + r * math.cos(angle)
            y = cy - r * math.sin(angle)
            points.append((x, y))
            angle += math.pi / 5

        return points

    def draw_star(self):
        # Carregar a imagem da estrela 3D
        star_image = Image.open(STAR_IMAGE_PATH)
        star_image = star_image.resize((RADIUS_OUTER * 2, RADIUS_OUTER * 2), Image.LANCZOS)
        self.star_photo = ImageTk.PhotoImage(star_image)

        # Desenhar a imagem da estrela centralizada
        self.canvas.create_image(CENTER_X, CENTER_Y, image=self.star_photo, anchor=tk.CENTER)

        # Desenhar os círculos indicando as áreas de clique
        for px, py in self.points:
            self.canvas.create_oval(px - POINT_RADIUS, py - POINT_RADIUS, px + POINT_RADIUS, py + POINT_RADIUS, outline='red')

    def on_click(self, event):
        x, y = event.x, event.y

        for i, (px, py) in enumerate(self.points):
            if self.is_within_click_range(x, y, px, py):
                if not self.clicked_points[i]:
                    self.handle_point_click(i, px, py)
                return

        for i, (px, py) in enumerate(self.new_star_points):
            if self.is_within_click_range(x, y, px, py):
                if not self.new_star_clicked_points[i]:
                    self.handle_point_click(i, px, py, new_star=True)
                return

    def handle_point_click(self, i, px, py, new_star=False):
        value = 2 ** (i + 1)
        print(f"Point {i + 1} value: {value}")
        self.canvas.create_text(px, py, text=str(value), fill='white')
        if new_star:
            self.new_star_clicked_points[i] = True
        else:
            self.clicked_points[i] = True
            if all(self.clicked_points):
                self.draw_new_star()

    def is_within_click_range(self, x, y, px, py, radius=POINT_RADIUS):
        return (x - px) ** 2 + (y - py) ** 2 <= radius ** 2

    def draw_new_star(self):
        new_center_x = NEW_STAR_OFFSET_X
        new_center_y = NEW_STAR_OFFSET_Y
        new_radius_outer = RADIUS_OUTER * NEW_STAR_SCALE
        new_radius_inner = RADIUS_INNER * NEW_STAR_SCALE
        self.new_star_points = self.calculate_star_points(new_center_x, new_center_y, new_radius_outer, new_radius_inner)
        self.new_star_clicked_points = [False] * len(self.new_star_points)

        for px, py in self.new_star_points:
            self.canvas.create_image(new_center_x, new_center_y, image=self.star_photo, anchor=tk.CENTER)

    def reset_stars(self):
        self.canvas.delete("all")
        self.initialize_stars()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("StarExp - Exponential Star")
    app = StarApp(root)
    root.mainloop()
