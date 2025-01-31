"""
display a single object, inert, at (100, 100)
"""
import arcade
import math
import random


BACKGROUND = arcade.color.ALMOND
WIDTH, LENGTH = 1200, 800

GOO = "media/goo.png"
SIZE_GOO = 50 # Taille en pixels, longueur comme largeur comme diametre

LINK = "media/link.png"
SIZE_LINK = (100, 10) # Longueur, largeur

CRITICAL_DISTANCE = 300 # Distance à partir de laquelle on considere les autres goos
PLATEFORM = "media/plateforme3.png"
#DETECTION_RADIUS = 15  # Rayon de détection en pixels (pour transparence)
#RAYON = 30             # Rayon pour contournement
#NB_BOID = 20

class Goo(arcade.Sprite):
    
    def __init__(self):
        # super().__init__(GOO)
        self.center_x, self.center_y = (x1, x2), (y1, y2) #positions a (t-dt, t)
        #angle et voisin aussi
        # self.speed = 150    # En pixel par seconde
        # self.angle = 0      # En degres
        # self.alpha = 255    # Initialement opaque

        # # Garde en mémoire la position precedente
        # self.prev_x, self.prev_y = self.center_x, self.center_y


    def on_update(self, delta_time, obstacles):

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

class Plateform(arcade.Sprite):
    # def __init__(self, x, y):
    #     super().__init__(OBSTACLE)
    #     self.center_x = x
    #     self.center_y = y

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
        

class Window(arcade.Window):

    # def __init__(self):
    #     super().__init__(WIDTH, LENGTH, "My first boid")
    #     arcade.set_background_color(BACKGROUND)
    #     self.set_location(800, 100)
    #     self.boids = arcade.SpriteList()

    #     # Liste pour stocker les obstacles
    #     self.obstacles = arcade.SpriteList()   

    #     # Garde en mémoire les touches maintenues enfoncées
    #     self.keys_pressed = set()           

    # def setup(self):
    #     for _ in range(NB_BOID):
    #         boid = Boid()
    #         self.boids.append(boid)

    #     # Créer la grille d'obstacles
    #     grid_size = 10      # 10x10 obstacles
    #     spacing = 80        # Espacement de 80px entre chaque obstacle
        
    #     for row in range(grid_size):
    #         for col in range(grid_size):
    #             # Calculer la position de chaque obstacle
    #             x = col * spacing + 40  # Décaler un peu pour centrer la grille
    #             y = row * spacing + 40  # Décaler un peu pour centrer la grille
    #             obstacle = Obstacle(x, y)
    #             self.obstacles.append(obstacle)

    # def on_draw(self):
    #     arcade.start_render()
    #     self.boids.draw()
    #     self.obstacles.draw()

    # def on_key_press(self, symbol, modifiers):
    #     self.keys_pressed.add(symbol)
    
    # def on_key_release(self, symbol, modifiers):
    #     self.keys_pressed.discard(symbol)

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when the user presses a mouse button. """

        if button == arcade.MOUSE_BUTTON_LEFT:
            return (x, y)


        # for boid in self.boids:
        #     boid.on_update(delta_time, self.obstacles)

window = Window()
window.setup()
arcade.run()