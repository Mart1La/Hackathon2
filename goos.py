"""
display a single object, inert, at (100, 100)
"""
import arcade
import math
import random

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


BACKGROUND = arcade.color.ALMOND
GOO = "media/goo.png"
SIZE_GOO = 50 # Taille en pixels, longueur comme largeur comme diametre

WIDTH, LENGTH = 1200, 700
CRITICAL_DISTANCE = 300 # Distance à partir de laquelle on considere les autres goos
PLATEFORME = "media/plateforme3.png"
TITLE = "Worlds of Goo"
PLATEFORME = "data/plateforme3.png"
Spread = 0.1

class Goo(arcade.Sprite):
    
    # def __init__(self):
    #     super().__init__(IMAGE)
    #     self.center_x, self.center_y = 100, 100
    #     self.speed = 150    # En pixel par seconde
    #     self.angle = 0      # En degres
    #     self.alpha = 255    # Initialement opaque

    #     # Garde en mémoire la position precedente
    #     self.prev_x, self.prev_y = self.center_x, self.center_y


    def on_update(self, delta_time):
        pass

        # self.center_x = (self.center_x + self.speed*delta_time * math.cos(math.radians(self.angle))) % WIDTH
        # self.center_y = (self.center_y + self.speed*delta_time * math.sin(math.radians(self.angle))) % LENGTH
        
        # # Permet de varier le cap
        # self.angle = (self.angle + random.randint(-4, 4)) % 360

        # # Vérification de la proximité d'un obstacle et rendre transparent si c'est le cas
        # for obstacle in obstacles:
        #     distance = math.sqrt((self.center_x - obstacle.center_x) ** 2 + (self.center_y - obstacle.center_y) ** 2)

        #     if distance <= RAYON:
        #         self.center_x = (self.center_x + (self.center_x - obstacle.center_x)*0.5*(1-(distance/RAYON))) % WIDTH
        #         self.center_y = (self.center_y + (self.center_y - obstacle.center_y)*0.5*(1-(distance/RAYON))) % LENGTH
        #         self.angle = self.angle + math.degrees(math.atan2(self.center_y-self.prev_y, self.center_x-self.prev_x))*0.01 # Pour amortir l'effet: v12

        #     if distance <= DETECTION_RADIUS:
        #         self.alpha = 100
        #         break
        # else:
        #     # Si aucun obstacle n'est proche, garder le boid opaque
        #     self.alpha = 255


        # # Mettre à jour la transparence du boid
        # self.color = (255, 255, 255, self.alpha)
        # self.prev_x = self.center_x
        # self.prev_y = self.center_y

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
        
        # Facteur d'échelle
        factor = self.target_width / SIZE_LINK[0]
        self.scale = factor

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

window = Window()
window.setup()
arcade.run()