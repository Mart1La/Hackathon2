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

# Constantes globales
BACKGROUND = arcade.color.ALMOND
GOO = "media/goo.png"
SIZE_GOO = 50   # Taille en pixels, longueur comme largeur comme diametre

WIDTH, LENGTH = 1200, 700
CRITICAL_DISTANCE = 300     # Distance à partir de laquelle on considere les autres goos
PLATEFORME = "media/plateforme3.png"
TITLE = "Worlds of Goo"
PLATEFORME = "data/plateforme3.png"
Spread = 0.1

LINK = "media/link.png"
SIZE_LINK = (100, 10) # Longueur, largeur du lien

# Définition des classes
class Goo(arcade.Sprite):
    
    def __init__(self, x, y):
        super().__init__(GOO)
        self.center_x, self.center_y = (x, x), (y, y) # selon le clic
        self.angle = 0
    
    def on_update(self, delta_time):
        
        # Rajouter une variation très faible au centre du goo
        # NOISE_POSITION = 5
        # self.center_x[1] += (1 - 2*random.random()) * NOISE_POSITION
        # self.center_y[1] += (1 - 2*random.random()) * NOISE_POSITION

        # # Pour rester dans la fenêtre ; à voir...
        # self.center_x %= HEIGHT
        # self.center_y %= WIDTH
        pass
    
class Link(arcade.Sprite):
    """ objet qui est un lien entre deux goos. on veut que la taille du lien (qui va être une image) change. 
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
        self.Goos = []
        self.Goos_adj = {}

    def setup(self):
        for n in range(0, 2):
            plateform = Plateform(n)
            self.plateforms.append(plateform)

    def on_draw(self):
        arcade.start_render()
        self.plateforms.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.Goos.append(Goo(int(x), int(y)))
        return super().on_mouse_press(int(x), int(y), button, modifiers)

    def on_update(self, delta_time):
        n = len(self.Goos)
        indices = list(range(n))
        indices = rd.shuffle(indices)

        for ind in indices:
            acc = g*np.array(0, -1)
            for duo in self.Good_adj[ind]:
                acc += (k/m) * np.array(
                    (np.sqrt((self.Goos[ind].center_y[1])**2 + (self.Goos[ind].center_x[1])**2) - np.sqrt((self.Goos[duo[0]].center_y[1])**2 + (self.Goos[duo[0]].center_x[1])**2) - duo[1])
                    * np.sin(np.arctan2((self.Goos[duo[0]].center_x[1] - self.Goos[ind].center_x[1]) , (self.Goos[ind].center_y[1] - self.Goos[duo[0]].center_y[1]))) ,
                    (np.sqrt((self.Goos[ind].center_y[1])**2 + (self.Goos[ind].center_x[1])**2) - np.sqrt((self.Goos[duo[0]].center_y[1])**2 + (self.Goos[duo[0]].center_x[1])**2) - duo[1])
                    * np.cos(np.arctan2((self.Goos[duo[0]].center_x[1] - self.Goos[ind].center_x[1]) , (self.Goos[ind].center_y[1] - self.Goos[duo[0]].center_y[1])))
                )
            newx_tdt = 2*self.Goos[ind].center_x[1] - self.Goos[ind].center_x[0] + acc[0]*(delta_time)**2
            newy_tdt = 2*self.Goos[ind].center_y[1] - self.Goos[ind].center_y[0] + acc[1]*(delta_time)**2
            self.Goos[ind].center_x = (self.Goos[ind].center_x[1], newx_tdt)
            self.Goos[ind].center_y = (self.Goos[ind].center_y[1], newy_tdt)


# Lancement du jeu
window = Window()
window.setup()
arcade.run()