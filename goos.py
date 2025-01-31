import arcade
import math
import random as rd
import numpy as np

#################################################################################################

### SYNTAXE A SUIVRE ###

Goos = [Goo() for k in range(20)]

Goos_adj = {3: [], 5: [(3, l0_3x5)], 17: [(3,l0_3x17), (5, l0_5x17)]}

Goos[17] # goo "numéro" 17
Goos[17].center_x[0] # position à t - dt du goo "numéro" 17
Goos[17].center_x[1] # position à t du goo "numéro" 17

Goos[Goos_adj[17][0][0]] # numéro du premier voisin du goo "numéro" 17
Goos[Goos_adj[17][0][1]] # l0 entre le goo "numéro" 17 et son premier voisin

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

    # def on_key_press(self, symbol, modifiers):
    #     self.keys_pressed.add(symbol)
    
    # def on_key_release(self, symbol, modifiers):
    #     self.keys_pressed.discard(symbol)

    def on_update(self, delta_time):
        pass

    #     # Si la flèche droite est pressée, on tourne vers la droite
    #     if arcade.key.RIGHT in self.keys_pressed:
    #         for boid in self.boids:
    #             boid.angle -= 5
        
    #     if arcade.key.UP in self.keys_pressed:
    #         for boid in self.boids:
    #             boid.speed += 50
    #         self.keys_pressed.discard(arcade.key.UP)
        
    #     if arcade.key.DOWN in self.keys_pressed:
    #         for boid in self.boids:
    #             boid.speed -= 50
    #         self.keys_pressed.discard(arcade.key.DOWN)

    #     for boid in self.boids:
    #         boid.on_update(delta_time, self.obstacles)

# Lancement du jeu
window = Window()
window.setup()
arcade.run()