import arcade
import math
import random as rd
import numpy as np

# Variables globales
BACKGROUND = arcade.color.SKY_BLUE
GOO = "data/goo.png"
SIZE_GOO = 50   # Taille en pixels, longueur comme largeur comme diamètre

WIDTH, LENGTH = 1200, 700
CRITICAL_DISTANCE = 300     # Distance à partir de laquelle on considère les autres goos
TITLE = "Worlds of Goo"
PLATEFORME = "data/plateforme3.png"
Spread = 0.1
g = 0.495
k = 100
m = 0.4

LINK = "data/link.png"
SIZE_LINK = (100, 10) # Longueur, largeur du lien

# Définition des classes
class Goo(arcade.Sprite):
    
    def __init__(self, x, y):
        super().__init__(GOO)
        self.center_x, self.center_y = x, y
        self.angle = 0

# class Link(arcade.Sprite):
#     def __init__(self, goo1: Goo, goo2: Goo):
#         super().__init__(LINK)
#         self.center_x = (goo1.center_x + goo2.center_x) / 2
#         self.center_y = (goo1.center_y + goo2.center_y) / 2
#         self.angle = (180 / math.pi) * (math.pi - math.atan2(goo1.center_y - goo2.center_y, goo1.center_x - goo2.center_x))
#         self.target_width = math.sqrt((goo1.center_x - goo2.center_x) ** 2 + (goo1.center_y - goo2.center_y) ** 2)
#         self.scale_x = self.target_width / SIZE_LINK[0]

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
        self.set_location(400, 100)
        self.plateforms = arcade.SpriteList()
        # self.links = arcade.SpriteList()
        self.Goos = arcade.SpriteList()
        self.Goos_adj = {}

    def setup(self):
        for n in range(0, 2):
            plateform = Plateform(n)
            self.plateforms.append(plateform)

    def on_draw(self):
        arcade.start_render()
        self.Goos.draw()
        self.plateforms.draw()
        # self.links.draw()  # Dessiner les liens

    def on_mouse_press(self, x, y, button, modifiers):
        new_goo = Goo(int(x), int(y))
        self.Goos.append(new_goo)

        # Create links to nearby goos based on a threshold distance
        for i, goo in enumerate(self.Goos):
            dist = np.sqrt((goo.center_x - new_goo.center_x) ** 2 + (goo.center_y - new_goo.center_y) ** 2)
            if dist < CRITICAL_DISTANCE:
                # link = Link(goo, new_goo)
                # self.links.append(link)
                if i not in self.Goos_adj:
                    self.Goos_adj[i] = []
                self.Goos_adj[i].append((len(self.Goos) - 1, dist))
                if len(self.Goos) - 1 not in self.Goos_adj:
                    self.Goos_adj[len(self.Goos) - 1] = []
                self.Goos_adj[len(self.Goos) - 1].append((i, dist))

    def on_update(self, delta_time):
        indices = list(range(len(self.Goos)))
        rd.shuffle(indices)

        for ind in indices:
            prev_pos_x, prev_pos_y = self.Goos[ind].center_x, self.Goos[ind].center_y  # Store previous position for velocity calculations
            acc = g*np.array([0, -1])
            for duo in self.Goos_adj[ind]:
                acc += (k/m) * np.array(
                    (np.sqrt((self.Goos[ind].center_y)**2 + (self.Goos[ind].center_x)**2) - np.sqrt((self.Goos[duo[0]].center_y)**2 + (self.Goos[duo[0]].center_x)**2) - duo[1])
                    * np.sin(np.atan2((self.Goos[duo[0]].center_x - self.Goos[ind].center_x) , (self.Goos[ind].center_y - self.Goos[duo[0]].center_y))) ,
                    (np.sqrt((self.Goos[ind].center_y)**2 + (self.Goos[ind].center_x)**2) - np.sqrt((self.Goos[duo[0]].center_y)**2 + (self.Goos[duo[0]].center_x)**2) - duo[1])
                    * np.cos(np.atan2((self.Goos[duo[0]].center_x - self.Goos[ind].center_x) , (self.Goos[ind].center_y - self.Goos[duo[0]].center_y)))
                )
            newx_tdt = 2*self.Goos[ind].center_x - prev_pos_x + acc[0]*(delta_time)**2
            newy_tdt = 2*self.Goos[ind].center_y - prev_pos_y + acc[1]*(delta_time)**2
            self.Goos[ind].center_x = int(newx_tdt)
            self.Goos[ind].center_y = int(newy_tdt)

# Lancement du jeu
window = Window()
window.setup()
arcade.run()
