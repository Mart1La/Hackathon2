import arcade
import math
import random as rd
import numpy as np

# Variables globales
BACKGROUND = arcade.color.SKY_BLUE
GOO = "data/goo.png"
SIZE_GOO = 50   # Taille en pixels, longueur comme largeur comme diamètre

WIDTH, LENGTH = 1200, 700
CRITICAL_DISTANCE = 200     # Distance à partir de laquelle on considère les autres goos
TITLE = "Worlds of Goo"
PLATEFORME = "data/plateforme3.png"
Spread = 0.1
g = 9.81 * 10
k = 0.5
m = 0.4

NOISE_POSITION = 0.2

LINK = "data/link.png"
SIZE_LINK = (100, 10) # Longueur, largeur du lien

# Définition des classes
class Goo(arcade.Sprite):
    
    def __init__(self, x, y):
        super().__init__(GOO)
        self.center_x, self.center_y = x, y
        self.center_x_previous, self.center_y_previous = x, y
        self.angle = 0
        self.connected_goo = []

    def connect(self, other_goo):
        self.connected_goo.append(other_goo)

    def draw_connection(self):
        for other_goo in self.connected_goo:
            arcade.draw_line(self.center_x, self.center_y, other_goo.center_x, other_goo.center_y, arcade.color.BLACK, 2)

class Link(arcade.Sprite):
    def __init__(self, goo1: Goo, goo2: Goo):
        super().__init__(LINK)
        self.center_x = (goo1.center_x + goo2.center_x) / 2
        self.center_y = (goo1.center_y + goo2.center_y) / 2
        self.angle = (180 / math.pi) * math.atan2(goo1.center_y - goo2.center_y, goo1.center_x - goo2.center_x)
        self.target_width = math.sqrt((goo1.center_x - goo2.center_x) ** 2 + (goo1.center_y - goo2.center_y) ** 2)
        self.scale_x = self.target_width / SIZE_LINK[0]

class Plateform(arcade.Sprite):
    def __init__(self, n):
        super().__init__(PLATEFORME)
        if n == 0:
            self.center_x = (WIDTH / 4) * (1 + rd.uniform(-Spread, Spread))
        else:
            self.center_x = (3 * WIDTH / 4) * (1 + rd.uniform(-Spread, Spread))
        self.center_y = (LENGTH / 2) * (1 + rd.uniform(-Spread, Spread))

class Window(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, LENGTH, TITLE)
        arcade.set_background_color(BACKGROUND)
        self.set_location(100, 30)
        self.plateforms = arcade.SpriteList()
        self.Goos = arcade.SpriteList()
        self.Goos_adj = {}
        self.zonestop = arcade.SpriteList()

    def setup(self):
        for n in range(0, 2):
            plateform = Plateform(n)
            self.plateforms.append(plateform)

    def on_draw(self):
        arcade.start_render()
        self.Goos.draw()
        self.plateforms.draw()
        for goo in self.Goos:
            goo.draw_connection()

    def on_mouse_press(self, x, y, button, modifiers):
        new_goo = Goo(int(x), int(y))
        self.Goos.append(new_goo)

        # Create links to nearby goos based on a threshold distance
        for i, goo in enumerate(self.Goos):
            dist = np.sqrt((goo.center_x - new_goo.center_x) ** 2 + (goo.center_y - new_goo.center_y) ** 2)
            if dist < CRITICAL_DISTANCE:
                goo.connect(new_goo)
                if i not in self.Goos_adj:
                    self.Goos_adj[i] = []
                self.Goos_adj[i].append((len(self.Goos) - 1, dist))
                if len(self.Goos) - 1 not in self.Goos_adj:
                    self.Goos_adj[len(self.Goos) - 1] = []
                self.Goos_adj[len(self.Goos) - 1].append((i, dist))

    def on_update(self, delta_time):
        for curr_goo in self.Goos:   
            curr_goo.center_x += (1 - 2*rd.random()) * NOISE_POSITION
            curr_goo.center_y += (1 - 2*rd.random()) * NOISE_POSITION

        for curr_goo in self.Goos:
            for plateform in self.plateforms:
                zone_center_x = plateform.center_x
                zone_center_y = plateform.center_y + 31
                if abs(curr_goo.center_x - zone_center_x) <= 40 and abs(curr_goo.center_y - zone_center_y) <= 40:
                    self.zonestop.append(curr_goo)

        DELTA_TIME = delta_time

        indices = list(range(len(self.Goos)))
        rd.shuffle(indices)

        for ind in indices:
            current_goo = self.Goos[ind]
            if current_goo not in self.zonestop:
                accx = 0
                # accy = -g
                accy = 0
                for duo in self.Goos_adj[ind]:
                    neighbor_goo = self.Goos[duo[0]]
                    vector = np.array([neighbor_goo.center_x, neighbor_goo.center_y]) - np.array([current_goo.center_x, current_goo.center_y])
                    dist_betw_goos = max(np.linalg.norm(vector), 1)
                    director_vector = vector / dist_betw_goos
                    accx += (k/m) * (dist_betw_goos - duo[1]) * np.dot(director_vector, np.array([1,0]))
                    accy += (k/m) * (dist_betw_goos - duo[1]) * np.dot(director_vector, np.array([0,1]))

                newx_tdt = 2*current_goo.center_x - current_goo.center_x_previous + accx*(DELTA_TIME)**2
                newy_tdt = 2*current_goo.center_y - current_goo.center_y_previous + accy*(DELTA_TIME)**2
                current_goo.center_x_previous, current_goo.center_x = current_goo.center_x, newx_tdt
                current_goo.center_y_previous, current_goo.center_y = current_goo.center_y, newy_tdt

# Lancement du jeu
window = Window()
window.setup()
arcade.run()
