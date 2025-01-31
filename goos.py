import arcade
import math
import random as rd
import numpy as np

#################################################################################################

### SYNTAXE A SUIVRE ###

# Goos = [Goo() for k in range(20)]

# Goos_adj = {3: [], 5: [(3, l0_3x5)], 17: [(3,l0_3x17), (5, l0_5x17)]}

# Goos[17] # goo "numéro" 17
# Goos[17].center_x[0] # position à t - dt du goo "numéro" 17
# Goos[17].center_x[1] # position à t du goo "numéro" 17

# Goos[Goos_adj[17][0][0]] # numéro du premier voisin du goo "numéro" 17
# Goos[Goos_adj[17][0][1]] # l0 entre le goo "numéro" 17 et son premier voisin

#################################################################################################

# Variables globales
BACKGROUND = arcade.color.SKY_BLUE
GOO = "data/goo.png"
SIZE_GOO = 50   # Taille en pixels, longueur comme largeur comme diametre

WIDTH, LENGTH = 1200, 700
CRITICAL_DISTANCE = 300     # Distance à partir de laquelle on considere les autres goos
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
        self.center_x, self.center_y = (x, x), (y, y) # selon le clic
        self.angle = 0
    
    def new_coordinates(self, delta_time, ind):
        acc = g*np.array([0, -1])
        for duo in window.Goos_adj[ind]:
            acc += (k/m) * np.array(
                (np.sqrt((window.Goos[ind].center_y[1])**2 + (window.Goos[ind].center_x[1])**2) - np.sqrt((window.Goos[duo[0]].center_y[1])**2 + (window.Goos[duo[0]].center_x[1])**2) - duo[1])
                * np.sin(np.arctan2((window.Goos[duo[0]].center_x[1] - window.Goos[ind].center_x[1]) , (window.Goos[ind].center_y[1] - window.Goos[duo[0]].center_y[1]))) ,
                (np.sqrt((window.Goos[ind].center_y[1])**2 + (window.Goos[ind].center_x[1])**2) - np.sqrt((window.Goos[duo[0]].center_y[1])**2 + (window.Goos[duo[0]].center_x[1])**2) - duo[1])
                * np.cos(np.arctan2((window.Goos[duo[0]].center_x[1] - window.Goos[ind].center_x[1]) , (window.Goos[ind].center_y[1] - window.Goos[duo[0]].center_y[1])))
            )
        newx_tdt = 2*window.Goos[ind].center_x[1] - window.Goos[ind].center_x[0] + acc[0]*(delta_time)**2
        newy_tdt = 2*window.Goos[ind].center_y[1] - window.Goos[ind].center_y[0] + acc[1]*(delta_time)**2
        window.Goos[ind].center_x = (window.Goos[ind].center_x[1], int(newx_tdt))
        window.Goos[ind].center_y = (window.Goos[ind].center_y[1], int(newy_tdt))

        # Rajouter une variation très faible au centre du goo
        # NOISE_POSITION = 5
        # self.center_x[1] += (1 - 2*random.random()) * NOISE_POSITION
        # self.center_y[1] += (1 - 2*random.random()) * NOISE_POSITION

        # Pour rester dans la fenêtre ; à voir...
        # self.center_x %= HEIGHT
        # self.center_y %= WIDTH
    
class Link(arcade.Sprite):
    """ 
    Objet qui est un lien entre deux goos. on veut que la taille du lien (qui va être une image) change. 
    On va donc demander au sprite qui sera un lien de changer de taille pour s'adapter aux goos.
    """
    def __init__(self, goo1 : Goo, goo2 : Goo):
        super().__init__(LINK)
        self.center_x, self.center_y = (goo1.center_x[1]+goo2.center_x[1])/2, (goo1.center_y[1]+goo2.center_y[1])/2
        self.angle = math.pi - math.atan2(goo1.center_y[1]-goo2.center_y[1], goo1.center_x[1]-goo2.center_x[1])

        # Largeur souhaitée en pixels
        self.target_width = math.sqrt((goo1.center_x[1]-goo2.center_x[1])**2+(goo1.center_y[1]-goo2.center_y[1])**2)  
        
        # Changement de la longueur du lien, on ne change pas la largeur
        self.scale_x = self.target_width / SIZE_LINK[0]


class Plateform(arcade.Sprite):

    def __init__(self, n):
        super().__init__(PLATEFORME)
        if n == 0:
            self.center_x = (WIDTH / 4) * (1+rd.uniform(-Spread, Spread))
        else : 
            self.center_x = (3 * WIDTH / 4) * (1+rd.uniform(-Spread, Spread))
        self.center_y = (LENGTH / 2)*(1+rd.uniform(-Spread, Spread))

class Window(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, LENGTH, TITLE)
        arcade.set_background_color(BACKGROUND)
        self.set_location(400, 100)
        self.plateforms = arcade.SpriteList()
        self.links = arcade.SpriteList()
        self.Goos = arcade.SpriteList()
        self.Goos_adj = {}

    def setup(self):
        for n in range(0, 2):
            plateform = Plateform(n)
            self.plateforms.append(plateform)

    def on_draw(self):
        arcade.start_render()
        self.plateforms.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        new_goo = Goo(int(x), int(y))
        self.Goos.append(new_goo)

        # Create links to nearby goos based on a threshold distance
        for i, goo in enumerate(self.Goos):
            dist = np.sqrt((goo.center_x[1] - new_goo.center_x[1])**2 + (goo.center_y[1] - new_goo.center_y[1])**2)
            if dist < CRITICAL_DISTANCE:
                link = Link(goo, new_goo)
                self.links.append(link)
                if i not in self.Goos_adj:
                    self.Goos_adj[i] = []
                self.Goos_adj[i].append((len(self.Goos)-1, dist))
                if len(self.Goos)-1 not in self.Goos_adj:
                    self.Goos_adj[len(self.Goos)-1] = []
                self.Goos_adj[len(self.Goos)-1].append((i, dist))

    def on_update(self, delta_time):
        indices = list(range(len(self.Goos)))
        rd.shuffle(indices)

        for ind in indices:
            self.Goos[ind].new_coordinates(delta_time, ind)


# Lancement du jeu

window = Window()
window.setup()
arcade.run()