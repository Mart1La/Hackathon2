import arcade
import math
import random as rd
import numpy as np

# Variables globales
BACKGROUND_COLOR = arcade.color.SKY_BLUE
BACKGROUND = "data/blue_sky.jpg"
GOO = "data/goo.png"
SIZE_GOO = 50   # Taille en pixels, longueur comme largeur comme diamètre

WIDTH, LENGTH = 1200, 700
CRITICAL_DISTANCE = 100     # Distance à partir de laquelle on considère les autres goos
TITLE = "Worlds of Goo"
PLATEFORME = "data/plateforme3.png"
Spread = 0.1
g = 9.81 * 5
k = 25
m = 1
d = 1

NOISE_POSITION = 0

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
            arcade.draw_line(self.center_x, self.center_y, other_goo.center_x, other_goo.center_y, arcade.color.BLACK, 5)

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
        # arcade.set_background_color(BACKGROUND_COLOR)
        self.set_location(100, 30)
        self.background = None
        self.plateforms = arcade.SpriteList()
        self.Goos = arcade.SpriteList()
        self.Goos_adj = {}
        self.zonestop = arcade.SpriteList()

    def setup(self):
        self.background = arcade.load_texture(BACKGROUND)

        for n in range(0, 2):
            plateform = Plateform(n)
            self.plateforms.append(plateform)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, WIDTH, LENGTH, self.background)
        self.Goos.draw()
        self.plateforms.draw()
        for goo in self.Goos:
            goo.draw_connection()

    def on_mouse_press(self, x, y, button, modifiers):
        new_goo = Goo(int(x), int(y))
        self.Goos.append(new_goo)

        # On a créé un dico d'adjacence qui contient les voisins de chaque sommet et la longueur à vide des ressorts
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
            if curr_goo not in self.zonestop:
                # faible bruit sur la position, intéressant pour les tests sans gravité
                curr_goo.center_x += (1 - 2*rd.random()) * NOISE_POSITION
                curr_goo.center_y += (1 - 2*rd.random()) * NOISE_POSITION
                # le goo doit se coller s'il est très proche de la plateforme, ie dans la zonestop
                for plateform in self.plateforms:
                    zone_center_x = plateform.center_x
                    zone_center_y = plateform.center_y + 31
                    if abs(curr_goo.center_x - zone_center_x) <= 20 and abs(curr_goo.center_y - zone_center_y) <= 20:
                        self.zonestop.append(curr_goo)

        DELTA_TIME = delta_time

        indices = list(range(len(self.Goos)))
        rd.shuffle(indices)

        for ind in indices:
            current_goo = self.Goos[ind]
            if current_goo not in self.zonestop:
                accx = 0
                accy = -g
                # accy = 0
                for duo in self.Goos_adj[ind]:
                    neighbor_goo = self.Goos[duo[0]]
                    vector = np.array([neighbor_goo.center_x, neighbor_goo.center_y]) - np.array([current_goo.center_x, current_goo.center_y])
                    dist_betw_goos = max(np.linalg.norm(vector), 1)
                    director_vector = vector / dist_betw_goos
                    accx += (k/m) * (dist_betw_goos - duo[1]) * np.dot(director_vector, np.array([1,0]))
                    accy += (k/m) * (dist_betw_goos - duo[1]) * np.dot(director_vector, np.array([0,1]))
                # ajout de frottements linéaires
                speed_vector = np.array([current_goo.center_x - current_goo.center_x_previous, current_goo.center_y - current_goo.center_y_previous])/DELTA_TIME
                friction_force = - (d/m) * speed_vector
                accx += np.dot(friction_force, np.array([1,0]))
                accy += np.dot(friction_force, np.array([0,1]))

                newx_tdt = 2*current_goo.center_x - current_goo.center_x_previous + accx*(DELTA_TIME)**2
                newy_tdt = 2*current_goo.center_y - current_goo.center_y_previous + accy*(DELTA_TIME)**2
                current_goo.center_x_previous, current_goo.center_x = current_goo.center_x, newx_tdt
                current_goo.center_y_previous, current_goo.center_y = current_goo.center_y, newy_tdt

# Lancement du jeu
window = Window()
window.setup()
arcade.run()
